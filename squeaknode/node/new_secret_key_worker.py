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

from squeak.core import CSqueak
from squeak.messages import msg_inv
from squeak.net import CInv

from squeaknode.core.util import get_hash
from squeaknode.core.util import squeak_matches_interest
from squeaknode.network.network_manager import NetworkManager
from squeaknode.network.peer import Peer
from squeaknode.node.squeak_controller import SqueakController


logger = logging.getLogger(__name__)

DEFAULT_MAX_QUEUE_SIZE = 1000
DEFAULT_UPDATE_INTERVAL_S = 1

HASH_LENGTH = 32
EMPTY_HASH = b'\x00' * HASH_LENGTH


class NewSecretKeyWorker:

    def __init__(self,
                 squeak_controller: SqueakController,
                 network_manager: NetworkManager,
                 ):
        self.squeak_controller = squeak_controller
        self.network_manager = network_manager
        self.stopped = threading.Event()

    def start_running(self):
        threading.Thread(
            target=self.handle_new_secret_keys,
            name="new_secret_keys_worker_thread",
        ).start()

    def stop_running(self):
        self.stopped.set()

    def handle_new_secret_keys(self):
        logger.info("Starting NewSecretKeyWorker...")
        for squeak_hash in self.squeak_controller.subscribe_new_secret_keys(
                self.stopped,
        ):
            logger.info("Handling new secret key for squeak hash: {!r}".format(
                squeak_hash.hex(),
            ))
            squeak = self.squeak_controller.get_squeak(squeak_hash)
            if squeak is not None:
                self.forward_secret_key(squeak)

    def forward_secret_key(self, squeak):
        logger.info("Forward new squeak: {!r}".format(
            get_hash(squeak).hex(),
        ))
        for peer in self.network_manager.get_connected_peers():
            if self.should_forward(squeak, peer):
                logger.info("Forwarding to peer: {}".format(
                    peer,
                ))
                squeak_hash = get_hash(squeak)
                inv = CInv(type=2, hash=squeak_hash)
                inv_msg = msg_inv(inv=[inv])
                peer.send_msg(inv_msg)
        logger.info("Finished checking peers to forward.")

    def should_forward(self, squeak: CSqueak, peer: Peer) -> bool:
        logger.info("""
        Checking if should forward for peer: {}
        with subscription: {}
        and squeak: {}
        with squeak address: {}
        """.format(
            peer,
            peer.subscription,
            squeak,
            str(squeak.GetAddress()),
        ))
        if peer.subscription is None:
            return False
        locator = peer.subscription.locator
        for interest in locator.vInterested:
            if squeak_matches_interest(squeak, interest):
                logger.info("Found a match!")
                return True
        return False
