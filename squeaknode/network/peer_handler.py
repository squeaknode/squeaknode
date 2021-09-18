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
import socket
import threading

from squeaknode.core.peer_address import PeerAddress
from squeaknode.network.connection import Connection
from squeaknode.network.peer import Peer


logger = logging.getLogger(__name__)


HANDSHAKE_TIMEOUT = 30


class PeerHandler():
    """Handles new peer connection.
    """

    def __init__(
            self,
            local_address,
            connection_manager,
            squeak_controller,
    ):
        self.local_address = local_address
        self.connection_manager = connection_manager
        self.squeak_controller = squeak_controller

    def handle_connection(
            self,
            peer_socket: socket.socket,
            address: PeerAddress,
            outgoing: bool,
    ):
        """Handle a new socket connection.

        This method blocks until the socket connection has stopped.
        """
        peer = Peer(
            peer_socket,
            self.local_address,
            address,
            outgoing,
            self.connection_manager.single_peer_changed_listener,
        )

        try:
            self.do_handshake(peer)
        except Exception:
            peer.stop()
            raise

        threading.Thread(
            target=self.start_connection,
            args=(peer,),
            name="handle_peer_connection_thread",
        ).start()

    def do_handshake(self, peer: Peer):
        """Do a handshake with a peer.
        """
        timer = HandshakeTimer(
            peer.stop,
            str(self),
        )
        timer.start_timer()

        if peer.outgoing:
            peer.send_version()
        # raise Exception("Fooooooo!")
        peer.receive_version()
        if not peer.outgoing:
            peer.send_version()

        peer.set_connected()
        logger.debug("HANDSHAKE COMPLETE-----------")
        timer.stop_timer()

    def start_connection(self, peer: Peer):
        """Start a connection
        """
        logger.debug(
            'Setting up connection for peer {}'.format(peer))
        try:
            with Connection(peer, self.squeak_controller).connect(
                    self.connection_manager
            ) as connection:
                connection.handle_connection()
        finally:
            peer.stop()
            logger.debug(
                'Stopped connection for peer {}.'.format(peer),
            )


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
