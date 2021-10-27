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

from squeaknode.core.peer_address import Network
from squeaknode.core.peer_address import PeerAddress


MIN_PEERS = 5
MAX_PEERS = 10
UPDATE_THREAD_SLEEP_TIME = 10


logger = logging.getLogger(__name__)


class PeerServer(object):
    """Accepts incoming connections from other peers in the network.
    """

    def __init__(self, peer_handler, port):
        self.peer_handler = peer_handler
        self.port = port
        self.listen_socket = socket.socket()

    def start(self):
        logger.info("Starting peer server with port: {}".format(
            self.port,
        ))
        # Start Listen thread
        threading.Thread(
            target=self.accept_connections,
            name="peer_server_listen_thread",
        ).start()

    def stop(self):
        logger.info("Stopping peer server listener thread...")
        self.listen_socket.shutdown(socket.SHUT_RDWR)
        self.listen_socket.close()

    def accept_connections(self):
        try:
            self.listen_socket.bind(('', self.port))
            self.listen_socket.listen()
            while True:
                peer_socket, address = self.listen_socket.accept()
                host, port = address
                peer_address = PeerAddress(
                    network=Network.IPV4,
                    host=host,
                    port=port,
                )
                peer_socket.setblocking(True)
                self.handle_connection(
                    peer_socket,
                    peer_address,
                )
        except Exception:
            logger.exception("Accept peer connections failed.")

    def handle_connection(
            self,
            peer_socket: socket.socket,
            peer_address: PeerAddress,
    ):
        """Handle a newly connected peer socket."""
        threading.Thread(
            target=self.peer_handler.handle_connection,
            args=(peer_socket, peer_address, False),
        ).start()
