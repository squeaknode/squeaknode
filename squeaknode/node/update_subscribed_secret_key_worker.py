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

from squeak.messages import msg_inv
from squeak.messages import MSG_SECRET_KEY
from squeak.net import CInv

from squeaknode.core.squeaks import get_hash
from squeaknode.network.network_manager import NetworkManager
from squeaknode.node.squeak_store import SqueakStore


logger = logging.getLogger(__name__)


class UpdateSubscribedSecretKeysWorker:

    def __init__(self, squeak_store: SqueakStore, network_manager: NetworkManager):
        self.squeak_store = squeak_store
        self.network_manager = network_manager
        self.stopped = threading.Event()

    def start_running(self):
        threading.Thread(
            target=self.handle_new_secret_keys,
            name="new_secret_keys_worker_thread",
            daemon=True,
        ).start()

    def stop_running(self):
        self.stopped.set()

    def handle_new_secret_keys(self):
        logger.debug("Starting UpdateSubscribedSecretKeysWorker...")
        for squeak in self.squeak_store.subscribe_new_secret_keys(
                self.stopped,
        ):
            logger.debug("Handling new secret key for squeak hash: {!r}".format(
                get_hash(squeak).hex(),
            ))
            self.forward_secret_key(squeak)

    def forward_secret_key(self, squeak):
        logger.debug("Forward new secret key for hash: {!r}".format(
            get_hash(squeak).hex(),
        ))
        for peer in self.network_manager.get_connected_peers():
            if peer.is_remote_subscribed(squeak):
                logger.debug("Forwarding to peer: {}".format(
                    peer,
                ))
                squeak_hash = get_hash(squeak)
                inv = CInv(type=MSG_SECRET_KEY, hash=squeak_hash)
                inv_msg = msg_inv(inv=[inv])
                peer.send_msg(inv_msg)
        logger.debug("Finished checking peers to forward.")
