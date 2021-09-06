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
from squeak.messages import MSG_SQUEAK
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


class NewSqueakWorker:

    def __init__(self,
                 squeak_controller: SqueakController,
                 network_manager: NetworkManager,
                 ):
        self.squeak_controller = squeak_controller
        self.network_manager = network_manager
        self.stopped = threading.Event()

    def start_running(self):
        threading.Thread(
            target=self.handle_new_squeaks,
            name="new_squeaks_worker_thread",
        ).start()

    def stop_running(self):
        self.stopped.set()

    def handle_new_squeaks(self):
        logger.debug("Starting NewSqueakWorker...")
        for squeak in self.squeak_controller.subscribe_new_squeaks(
                self.stopped,
        ):
            logger.debug("Handling new squeak: {!r}".format(
                get_hash(squeak).hex(),
            ))
            self.forward_squeak(squeak)

    def forward_squeak(self, squeak):
        logger.debug("Forward new squeak: {!r}".format(
            get_hash(squeak).hex(),
        ))
        for peer in self.network_manager.get_connected_peers():
            if self.should_forward(squeak, peer):
                logger.debug("Forwarding to peer: {}".format(
                    peer,
                ))
                squeak_hash = get_hash(squeak)
                inv = CInv(type=MSG_SQUEAK, hash=squeak_hash)
                inv_msg = msg_inv(inv=[inv])
                peer.send_msg(inv_msg)
        logger.debug("Finished checking peers to forward.")

    def should_forward(self, squeak: CSqueak, peer: Peer) -> bool:
        logger.debug("""
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
                logger.debug("Found a match!")
                return True
        return False
