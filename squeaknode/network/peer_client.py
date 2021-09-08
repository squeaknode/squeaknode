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

import socks

from squeaknode.core.peer_address import PeerAddress


SOCKET_CONNECT_TIMEOUT = 5


logger = logging.getLogger(__name__)


class PeerClient(object):
    """Creates outgoing connections to other peers in the network.
    """

    def __init__(self, peer_handler, tor_proxy_ip, tor_proxy_port):
        self.peer_handler = peer_handler
        self.tor_proxy_ip = tor_proxy_ip
        self.tor_proxy_port = tor_proxy_port

    def make_connection(self, address: PeerAddress):
        logger.info('Making connection to {}'.format(address))
        try:
            peer_socket = self.get_socket()
            logger.info('Trying to connect socket to {}'.format(address))
            peer_socket.settimeout(SOCKET_CONNECT_TIMEOUT)
            peer_socket.connect(address)
            peer_socket.setblocking(True)
            self.peer_handler.handle_connection(
                peer_socket, address, outgoing=True)
        except Exception:
            logger.exception('Failed to make connection to {}'.format(address))

    def connect_address(self, address: PeerAddress):
        """Connect to new address."""
        logger.info('Connecting to peer with address {}'.format(address))
        threading.Thread(
            target=self.make_connection,
            args=(address,),
            name="peer_client_connection_thread",
        ).start()

    def get_socket(self):
        if self.tor_proxy_ip:
            s = socks.socksocket()  # Same API as socket.socket in the standard lib
            s.set_proxy(socks.SOCKS5, self.tor_proxy_ip, self.tor_proxy_port)
            return s
        return socket.socket()
