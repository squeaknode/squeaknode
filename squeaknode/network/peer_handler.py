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

from squeaknode.core.peer_address import PeerAddress
from squeaknode.network.connection import Connection
from squeaknode.network.peer import Peer


logger = logging.getLogger(__name__)


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

    # def handle_connection(self, peer_socket: socket.socket, address: PeerAddress, outgoing: bool):
    #     threading.Thread(
    #         target=self.handle_connection_fn,
    #         args=(self.squeak_controller, peer_socket, address, outgoing,),
    #     ).start()

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

        logger.debug(
            'Setting up connection for peer address {} ...'.format(address))
        try:
            with Connection(peer, self.squeak_controller).connect(
                    self.connection_manager
            ) as connection:
                connection.handle_connection()
        finally:
            peer.stop()
            logger.debug(
                'Stopped connection for peer address {}.'.format(address))
