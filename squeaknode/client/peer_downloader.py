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
from typing import List

from squeak.core.keys import SqueakPublicKey

from squeaknode.client.peer_client import PeerClient
from squeaknode.core.squeak_peer import SqueakPeer
from squeaknode.node.squeak_store import SqueakStore

logger = logging.getLogger(__name__)


DOWNLOAD_TIMEOUT_S = 10


class PeerDownloader:

    def __init__(self, peer: SqueakPeer, squeak_store: SqueakStore, config):
        self.peer = peer
        self.client = PeerClient(peer, config)
        self.squeak_store = squeak_store
        self.config = config

    def download_squeaks(
            self,
            min_block: int,
            max_block: int,
            pubkeys: List[SqueakPublicKey],
    ) -> None:
        squeak_hashes = self.client.lookup(min_block, max_block, pubkeys)
        for squeak_hash in squeak_hashes:
            # Download the squeak if not already owned.
            if not self.squeak_store.get_squeak(squeak_hash):
                squeak = self.client.get_squeak(squeak_hash)
                if squeak and \
                   squeak.nBlockHeight >= min_block and \
                   squeak.nBlockHeight <= max_block and \
                   squeak.GetPubKey() in pubkeys:
                    self.squeak_store.save_squeak(squeak)
            # Download the secret key is not already unlocked.
            if not self.squeak_store.get_squeak_secret_key(squeak_hash):
                # TODO
                pass
