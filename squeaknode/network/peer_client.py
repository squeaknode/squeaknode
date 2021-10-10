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
import queue
import socket
import threading

import socks

from squeaknode.core.peer_address import Network
from squeaknode.core.peer_address import PeerAddress


SOCKET_CONNECT_TIMEOUT = 30


logger = logging.getLogger(__name__)


class PeerClient(object):
    """Creates outgoing connections to other peers in the network.
    """

    def __init__(self, peer_handler, tor_proxy_ip, tor_proxy_port):
        self.peer_handler = peer_handler
        self.tor_proxy_ip = tor_proxy_ip
        self.tor_proxy_port = tor_proxy_port

    def connect_address(self, address: PeerAddress):
        logger.info('Making connection to {}'.format(address))
        result_queue: queue.Queue = queue.Queue()
        threading.Thread(
            target=self.make_connection,
            args=(address, result_queue,),
        ).start()

        # Wait for connect result from the queue.
        connect_result = result_queue.get()
        logger.debug("connect_result: {}".format(connect_result))
        if connect_result.failure is not None:
            raise connect_result.failure

    def connect_address_async(self, address: PeerAddress):
        logger.info('Making connection async to {}'.format(address))
        result_queue: queue.Queue = queue.Queue()
        threading.Thread(
            target=self.make_connection,
            args=(address, result_queue,),
        ).start()

    def make_connection(self, address: PeerAddress, result_queue: queue.Queue):
        logger.info('Conecting to address: {}'.format(address))
        try:
            peer_socket = self.get_socket(address)
            peer_socket.settimeout(SOCKET_CONNECT_TIMEOUT)
            connect_address = (address.host, address.port)
            peer_socket.connect(connect_address)
            peer_socket.setblocking(True)
            self.handle_connection(
                peer_socket,
                address,
                result_queue,
            )
        except Exception as e:
            logger.exception('Failed to connect to {}'.format(address))
            result_queue.put(ConnectPeerResult.from_failure(e))

    def handle_connection(
            self,
            peer_socket: socket.socket,
            peer_address: PeerAddress,
            result_queue: queue.Queue,
    ):
        """Handle a newly connected peer socket."""
        self.peer_handler.handle_connection(
            peer_socket,
            peer_address,
            outgoing=True,
            result_queue=result_queue,
        )

    def get_socket(self, address: PeerAddress):
        if address.network not in [
                Network.IPV4,
                Network.IPV6,
                Network.TORV3,
        ]:
            raise Exception("Unsupported network: {}".format(address.network))
        if address.network == Network.TORV3 and self.tor_proxy_ip is None:
            raise Exception(
                "Unable to connect to tor address without tor proxy ip configured.")
        if address.network == Network.TORV3 and self.tor_proxy_port is None:
            raise Exception(
                "Unable to connect to tor address without tor proxy port configured.")
        if address.network == Network.TORV3:
            s = socks.socksocket()  # Same API as socket.socket in the standard lib
            s.set_proxy(socks.SOCKS5, self.tor_proxy_ip, self.tor_proxy_port)
            return s
        return socket.socket()


class ConnectPeerResult(object):
    """Result of a connect peer attempt.
    """

    def __init__(
            self,
            success: PeerAddress = None,
            failure: Exception = None,
    ):
        self.success = success
        self.failure = failure

    @classmethod
    def from_success(cls, success):
        return cls(success=success)

    @classmethod
    def from_failure(cls, failure):
        return cls(failure=failure)

    def __repr__(self):
        return "ConnectPeerResult: \
        success: {} \
        failure: {}".format(
            self.success,
            self.failure,
        )
