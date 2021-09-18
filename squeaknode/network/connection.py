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
from contextlib import contextmanager

from squeak.messages import msg_getaddr
from squeak.messages import msg_subscribe

from squeaknode.network.peer import Peer
from squeaknode.network.peer_message_handler import PeerMessageHandler


logger = logging.getLogger(__name__)


class Connection(object):
    """Handles lifecycle of a connection to a peer.
    """

    def __init__(self, peer: Peer, squeak_controller):
        self.peer = peer
        self.squeak_controller = squeak_controller

    @contextmanager
    def connect(self, connection_manager):
        logger.debug("Adding peer.")
        connection_manager.add_peer(self.peer)
        try:
            logger.debug("Yielding peer.")
            yield self
        except Exception:
            logger.exception("Peer connection failed.")
        finally:
            logger.debug("Removing peer.")
            connection_manager.remove_peer(self.peer)
            self.peer.stop()
            # TODO: Set a stop event here.

    def handle_connection(self):
        self.initial_sync()
        self.handle_messages()

    def initial_sync(self):
        self.update_addrs()
        self.update_subscription()

    def update_subscription(self):
        locator = self.squeak_controller.get_interested_locator()
        subscribe_msg = msg_subscribe(
            locator=locator,
        )
        self.peer.send_msg(subscribe_msg)

    def update_addrs(self):
        getaddr_msg = msg_getaddr()
        self.peer.send_msg(getaddr_msg)

    def handle_messages(self):
        peer_message_handler = PeerMessageHandler(
            self.peer,
            self.squeak_controller,
        )
        peer_message_handler.handle_msgs()
