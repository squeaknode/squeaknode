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
from abc import ABC
from abc import abstractmethod
from typing import List
from typing import Optional

from squeak.core import CSqueak
from squeak.core.keys import SqueakPublicKey

from squeaknode.client.peer_client import PeerClient
from squeaknode.core.squeak_peer import SqueakPeer
from squeaknode.core.squeaks import get_hash
from squeaknode.node.squeak_store import SqueakStore

logger = logging.getLogger(__name__)


DOWNLOAD_TIMEOUT_S = 10


class PeerDownloader(ABC):

    def __init__(
            self,
            peer: SqueakPeer,
            squeak_store: SqueakStore,
            proxy_host: Optional[str],
            proxy_port: Optional[int],
    ):
        self.peer = peer
        self.proxy_host = proxy_host
        self.proxy_port = proxy_port
        self.client = PeerClient(peer, proxy_host, proxy_port)
        self.squeak_store = squeak_store

    @abstractmethod
    def get_hashes(self) -> List[bytes]:
        """Get list of squeak hashes to download.
        """

    @abstractmethod
    def is_squeak_wanted(self, squeak: CSqueak) -> bool:
        """Return true if squeak is supposed to be downloaded.
        """

    def download_async(self) -> None:
        thread = threading.Thread(
            target=self.download,
            args=(),
        )
        thread.start()

    def download(self) -> None:
        squeak_hashes = self.get_hashes()
        for squeak_hash in squeak_hashes:
            # Download the squeak if not already owned.
            self.get_squeak(squeak_hash)
            # Download the secret key if not already unlocked.
            self.get_secret_key(squeak_hash)
            # Download the offer if not already unlocked.
            self.get_offer(squeak_hash)

    def get_squeak(self, squeak_hash: bytes) -> None:
        # Download the squeak if not already owned.
        if self.squeak_store.get_squeak(squeak_hash):
            return
        squeak = self.client.get_squeak(squeak_hash)
        if squeak and self.is_squeak_wanted(squeak):
            self.squeak_store.save_squeak(squeak)

    def get_secret_key(self, squeak_hash: bytes) -> None:
        # Get the squeak from the database.
        squeak = self.squeak_store.get_squeak(squeak_hash)
        if squeak and self.is_squeak_wanted(squeak):
            # Download the secret key is not already unlocked.
            if self.squeak_store.get_squeak_secret_key(squeak_hash):
                return
            secret_key = self.client.get_secret_key(squeak_hash)
            if secret_key:
                self.squeak_store.save_secret_key(squeak_hash, secret_key)

    def get_offer(self, squeak_hash: bytes) -> None:
        # Get the squeak from the database.
        squeak = self.squeak_store.get_squeak(squeak_hash)
        if squeak and self.is_squeak_wanted(squeak):
            # Download the secret key is not already unlocked.
            if self.squeak_store.get_squeak_secret_key(squeak_hash):
                return
            offer = self.client.get_offer(squeak_hash)
            if offer:
                self.squeak_store.handle_offer(
                    squeak,
                    offer,
                    self.peer.address,
                )


class RangeDownloader(PeerDownloader):

    def __init__(
            self,
            peer: SqueakPeer,
            squeak_store: SqueakStore,
            proxy_host: Optional[str],
            proxy_port: Optional[int],
            min_block: int,
            max_block: int,
            pubkeys: List[SqueakPublicKey],
    ):
        super().__init__(peer, squeak_store, proxy_host, proxy_port)
        self.min_block = min_block
        self.max_block = max_block
        self.pubkeys = pubkeys

    def get_hashes(self) -> List[bytes]:
        return self.client.lookup(
            self.min_block,
            self.max_block,
            self.pubkeys,
        )

    def is_squeak_wanted(self, squeak: CSqueak) -> bool:
        return squeak.nBlockHeight >= self.min_block and \
            squeak.nBlockHeight <= self.max_block and \
            squeak.GetPubKey() in self.pubkeys


class SingleDownloader(PeerDownloader):

    def __init__(
            self,
            peer: SqueakPeer,
            squeak_store: SqueakStore,
            proxy_host: Optional[str],
            proxy_port: Optional[int],
            squeak_hash: bytes,
    ):
        super().__init__(peer, squeak_store, proxy_host, proxy_port)
        self.squeak_hash = squeak_hash

    def get_hashes(self) -> List[bytes]:
        return [self.squeak_hash]

    def is_squeak_wanted(self, squeak: CSqueak) -> bool:
        return get_hash(squeak) == self.squeak_hash
