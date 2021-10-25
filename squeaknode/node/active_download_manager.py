# MIT License
#
# Copyright (c) 2020 Jonathan Zernik
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.
import logging
import threading
import uuid
from abc import ABC
from abc import abstractmethod
from concurrent.futures import ThreadPoolExecutor
from concurrent.futures import TimeoutError
from typing import Dict
from typing import Optional

from squeak.core import CSqueak
from squeak.messages import msg_getdata
from squeak.messages import msg_getsqueaks
from squeak.net import CInterested
from squeak.net import CInv
from squeak.net import CSqueakLocator

from squeaknode.core.download_result import DownloadResult
from squeaknode.core.interests import squeak_matches_interest
from squeaknode.core.squeaks import get_hash

logger = logging.getLogger(__name__)


DOWNLOAD_TIMEOUT_S = 10


class ActiveDownload(ABC):

    def __init__(self, limit: int):
        self.limit = limit
        # self.timeout_s = timeout_s
        self.count = 0
        self._lock = threading.Lock()
        self.stopped = threading.Event()

    @abstractmethod
    def is_interested(self, squeak: CSqueak) -> bool:
        """Return True if the given squeak matches the download interest."""

    @abstractmethod
    def initiate_download(self, broadcast_fn) -> None:
        """Broadcast a message to peers to get data."""

    def increment(self) -> None:
        with self._lock:
            self.count += 1
            if self.count >= self.limit:
                self.stopped.set()

    # # TODO: remove this method.
    # def is_under_limit(self) -> bool:
    #     with self._lock:
    #         return self.count < self.limit

    def wait_for_stop(self) -> None:
        self.stopped.wait()

    def get_result(self) -> DownloadResult:
        return DownloadResult(
            number_downloaded=self.count,
            number_requested=self.limit,
            request_time_s=-1,
        )


class RangeDownload(ActiveDownload):

    def __init__(self, limit: int, interest: CInterested):
        self.interest = interest
        super().__init__(limit)

    def is_interested(self, squeak: CSqueak) -> bool:
        return squeak_matches_interest(squeak, self.interest)

    def initiate_download(self, broadcast_fn) -> None:
        locator = CSqueakLocator(
            vInterested=[self.interest],
        )
        getsqueaks_msg = msg_getsqueaks(
            locator=locator,
        )
        broadcast_fn(getsqueaks_msg)


class HashDownload(ActiveDownload):

    def __init__(self, limit: int, squeak_hash: bytes):
        self.squeak_hash = squeak_hash
        super().__init__(limit)

    def is_interested(self, squeak: CSqueak) -> bool:
        return self.squeak_hash == get_hash(squeak)

    def initiate_download(self, broadcast_fn) -> None:
        invs = [
            CInv(type=1, hash=self.squeak_hash)
        ]
        getdata_msg = msg_getdata(
            inv=invs,
        )
        broadcast_fn(getdata_msg)


class ActiveDownloadManager:

    def __init__(self, broadcast_fn):
        self.downloads: Dict[str, ActiveDownload] = dict()
        # self.interests: Dict[str, ActiveDownload] = ExpiringDict(
        #     max_len=100, max_age_seconds=10)
        self.executor = ThreadPoolExecutor(max_workers=10)
        self.broadcast_fn = broadcast_fn

    def lookup_counter(self, squeak: CSqueak) -> Optional[ActiveDownload]:
        for name, interest in self.downloads.items():
            if interest.is_interested(squeak):
                return interest
        return None

    def run_download(self, download: ActiveDownload) -> DownloadResult:
        name_key = "download_key_{}".format(uuid.uuid1())
        self.downloads[name_key] = download
        future = self.executor.submit(self.download_task, download)
        try:
            return future.result(DOWNLOAD_TIMEOUT_S)
        except TimeoutError:
            return download.get_result()
        finally:
            del self.downloads[name_key]

    def download_task(self, download: ActiveDownload) -> DownloadResult:
        download.initiate_download(self.broadcast_fn)
        download.wait_for_stop()
        return download.get_result()

    def download_interest(self, limit: int, interest: CInterested) -> DownloadResult:
        download = RangeDownload(limit, interest)
        return self.run_download(download)

    def download_hash(self, limit: int, squeak_hash: bytes) -> DownloadResult:
        download = HashDownload(limit, squeak_hash)
        return self.run_download(download)
