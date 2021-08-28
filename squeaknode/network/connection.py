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
from contextlib import contextmanager

from squeak.messages import msg_subscribe

from squeaknode.network.peer import Peer
from squeaknode.network.peer_message_handler import PeerMessageHandler

HANDSHAKE_TIMEOUT = 5


logger = logging.getLogger(__name__)


class Connection(object):
    """Handles lifecycle of a connection to a peer.
    """

    def __init__(self, peer: Peer, squeak_controller):
        self.peer = peer
        self.squeak_controller = squeak_controller

    @contextmanager
    def connect(self, connection_manager):
        self.start_receiving_msgs()
        self.handshake()
        logger.info("Adding peer.")
        connection_manager.add_peer(self.peer)
        try:
            logger.info("Yielding peer.")
            yield self
        except Exception:
            logger.exception("Peer connection failed.")
        finally:
            logger.info("Removing peer.")
            connection_manager.remove_peer(self.peer)

    def handle_connection(self):
        self.initial_sync()
        self.handle_messages()

    def initial_sync(self):
        # TODO: getaddrs from peer.
        self.update_subscription()

    def update_subscription(self):
        locator = self.squeak_controller.get_interested_locator()
        subscribe_msg = msg_subscribe(
            locator=locator,
        )
        self.peer.send_msg(subscribe_msg)

    def start_receiving_msgs(self):
        threading.Thread(
            target=self.peer.recv_msgs,
            args=(),
        ).start()

    def handshake(self):
        timer = HandshakeTimer(
            self.peer.stop,
            str(self),
        )
        timer.start_timer()

        if self.peer.outgoing:
            self.peer.send_version()
        self.peer.receive_version()
        if not self.peer.outgoing:
            self.peer.send_version()

        self.peer.set_connected()
        logger.info("HANDSHAKE COMPLETE-----------")
        timer.stop_timer()

    def handle_messages(self):
        peer_message_handler = PeerMessageHandler(
            self.peer,
            self.squeak_controller,
        )
        peer_message_handler.handle_msgs()


class HandshakeTimer:
    """Stop the peer if handshake is not complete before timeout.
    """

    def __init__(self,
                 stop_fn,
                 peer_name,
                 ):
        self.stop_fn = stop_fn
        self.peer_name = peer_name
        self.timer = None

    def start_timer(self):
        self.timer = threading.Timer(
            HANDSHAKE_TIMEOUT,
            self.stop_peer,
        )
        self.timer.name = "handshake_timere_thread_{}".format(self.peer_name)
        self.timer.start()

    def stop_timer(self):
        logger.debug("Canceling handshake timer.")
        self.timer.cancel()

    def stop_peer(self):
        logger.info("Closing peer from handshake timer.")
        self.stop_fn()
