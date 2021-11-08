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
import time
import uuid
from abc import ABC
from abc import abstractmethod
from concurrent.futures import ThreadPoolExecutor
from concurrent.futures import TimeoutError
from typing import Dict
from typing import Optional

from squeak.messages import msg_getdata
from squeak.messages import msg_getsqueaks
from squeak.messages import MsgSerializable
from squeak.net import CInterested
from squeak.net import CInv
from squeak.net import CSqueakLocator

from squeaknode.core.download_result import DownloadResult
from squeaknode.node.downloaded_object import DownloadedObject

logger = logging.getLogger(__name__)


DOWNLOAD_TIMEOUT_S = 10


class ActiveDownload(ABC):

    def __init__(self, limit: int):
        self.limit = limit
        self.count = 0
        self._lock = threading.Lock()
        self.stopped = threading.Event()
        self.num_peers = 0
        self.start_time_ms: Optional[int] = None

    @abstractmethod
    def is_interested(self, downloaded_object: DownloadedObject) -> bool:
        """Return True if the given squeak matches the download interest."""

    @abstractmethod
    def get_download_msg(self) -> MsgSerializable:
        """Get the message to send to peers to get download response."""

    def initiate_download(self, broadcast_fn) -> None:
        self.start_time_ms = int(time.time() * 1000)
        msg = self.get_download_msg()
        self.num_peers = broadcast_fn(msg)
        if self.num_peers == 0:
            self.mark_complete()

    def increment(self) -> None:
        with self._lock:
            self.count += 1
            if self.count >= self.limit:
                self.mark_complete()

    def mark_complete(self):
        self.stopped.set()

    def cancel(self):
        self.stopped.set()

    def get_elapsed_time_ms(self):
        if self.start_time_ms is None:
            return 0
        end_time_ms = int(time.time() * 1000)
        return end_time_ms - self.start_time_ms

    def wait_for_complete(self, timeout_s: int) -> None:
        self.stopped.wait(timeout=timeout_s)

    def get_result(self) -> DownloadResult:
        return DownloadResult(
            number_downloaded=self.count,
            number_requested=self.limit,
            elapsed_time_ms=self.get_elapsed_time_ms(),
            number_peers=self.num_peers,
        )


class InterestDownload(ActiveDownload):

    def __init__(self, limit: int, interest: CInterested):
        self.interest = interest
        super().__init__(limit)

    def is_interested(self, downloaded_object: DownloadedObject) -> bool:
        return downloaded_object.matches_requested_squeak_range(self.interest)

    def get_download_msg(self) -> MsgSerializable:
        locator = CSqueakLocator(
            vInterested=[self.interest],
        )
        return msg_getsqueaks(
            locator=locator,
        )


class HashDownload(ActiveDownload):

    def __init__(self, squeak_hash: bytes):
        self.squeak_hash = squeak_hash
        super().__init__(1)

    def is_interested(self, downloaded_object: DownloadedObject) -> bool:
        return downloaded_object.matches_requested_squeak_hash(self.squeak_hash)

    def get_download_msg(self) -> MsgSerializable:
        invs = [
            CInv(type=1, hash=self.squeak_hash)
        ]
        return msg_getdata(
            inv=invs,
        )


class OffersDownload(ActiveDownload):

    def __init__(self, limit: int, squeak_hash: bytes):
        self.squeak_hash = squeak_hash
        super().__init__(limit)

    def is_interested(self, downloaded_object: DownloadedObject) -> bool:
        return downloaded_object.matches_requested_offer_hash(self.squeak_hash)

    def get_download_msg(self) -> MsgSerializable:
        invs = [
            CInv(type=2, hash=self.squeak_hash)
        ]
        return msg_getdata(inv=invs)


class ActiveDownloadManager:

    def __init__(self):
        self.downloads: Dict[str, ActiveDownload] = dict()
        self.executor = None
        self.broadcast_fn = None

    def start(self, broadcast_fn):
        logger.info("Starting Download Manager...")
        self.broadcast_fn = broadcast_fn
        self.executor = ThreadPoolExecutor(max_workers=10)

    def stop(self):
        for download in self.downloads.values():
            download.cancel()
        logger.info("Stopping Download Manager...")
        self.executor.shutdown(wait=True)
        logger.info("Stopped Download Manager.")

    def lookup_counter(self, downloaded_object: DownloadedObject) -> Optional[ActiveDownload]:
        for name, interest in self.downloads.items():
            if interest.is_interested(downloaded_object):
                return interest
        return None

    def run_download(self, download: ActiveDownload) -> DownloadResult:
        name_key = "download_key_{}".format(uuid.uuid1())
        self.downloads[name_key] = download
        future = self.executor.submit(self.download_task, download)
        try:
            return future.result()
        except TimeoutError:
            return download.get_result()
        finally:
            del self.downloads[name_key]

    def download_task(self, download: ActiveDownload) -> DownloadResult:
        download.initiate_download(self.broadcast_fn)
        download.wait_for_complete(DOWNLOAD_TIMEOUT_S)
        return download.get_result()

    def download_interest(self, limit: int, interest: CInterested) -> DownloadResult:
        download = InterestDownload(limit, interest)
        return self.run_download(download)

    def download_hash(self, squeak_hash: bytes) -> DownloadResult:
        download = HashDownload(squeak_hash)
        return self.run_download(download)

    def download_offers(self, limit: int, squeak_hash: bytes) -> DownloadResult:
        download = OffersDownload(limit, squeak_hash)
        return self.run_download(download)
