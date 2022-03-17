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

from squeak.core.keys import SqueakPublicKey

from squeaknode.client.peer_downloader import PeerDownloader
from squeaknode.node.squeak_store import SqueakStore

logger = logging.getLogger(__name__)


DOWNLOAD_TIMEOUT_S = 10


class NetworkController:

    def __init__(self, squeak_store: SqueakStore, config):
        self.squeak_store = squeak_store
        self.config = config

    def download_timeline(self) -> None:
        min_block = 0  # TODO
        max_block = 999999999999  # TODO
        followed_public_keys = self.squeak_store.get_followed_public_keys()
        peers = self.squeak_store.get_autoconnect_peers()
        for peer in peers:
            downloader = PeerDownloader(peer, self.squeak_store, self.config)
            downloader.download_squeaks(
                min_block, max_block, followed_public_keys)

    def download_pubkey_squeaks(self, pubkey: SqueakPublicKey) -> None:
        min_block = 0  # TODO
        max_block = 999999999999  # TODO
        peers = self.squeak_store.get_autoconnect_peers()
        for peer in peers:
            downloader = PeerDownloader(peer, self.squeak_store, self.config)
            downloader.download_squeaks(
                min_block, max_block, [pubkey])
