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
from typing import Iterable
from typing import List
from typing import Optional

import squeak.params
from squeak.messages import MsgSerializable
from squeak.net import CSqueakLocator

from squeaknode.core.peer_address import Network
from squeaknode.core.peer_address import PeerAddress
from squeaknode.network.connection_manager import ConnectionManager
from squeaknode.network.peer import Peer
from squeaknode.network.peer_client import PeerClient
from squeaknode.network.peer_handler import PeerHandler
from squeaknode.network.peer_server import PeerServer


MIN_PEERS = 5
MAX_PEERS = 10
UPDATE_THREAD_SLEEP_TIME = 10


logger = logging.getLogger(__name__)


class NetworkManager(object):
    """Interface for doing things involving the network.
    """

    def __init__(self, config):
        self.config = config
        self.external_host = self.config.server.external_address
        self.local_ip = socket.gethostbyname('localhost')
        self.local_port = self.config.server.port or squeak.params.params.DEFAULT_PORT
        self.peer_server = None
        self.peer_client = None
        self.tor_proxy_ip = self.config.tor.proxy_ip
        self.tor_proxy_port = self.config.tor.proxy_port
        self.connection_manager = ConnectionManager(self.local_address)

    def start(self, squeak_controller):
        peer_handler = PeerHandler(
            self.connection_manager,
            squeak_controller,
        )
        self.peer_server = PeerServer(
            peer_handler,
            self.local_port,
        )
        self.peer_client = PeerClient(
            peer_handler,
            self.tor_proxy_ip,
            self.tor_proxy_port,
        )
        self.peer_server.start()

    def stop(self):
        self.peer_server.stop()
        self.connection_manager.stop_all_connections()

    def connect_peer_sync(self, peer_address: PeerAddress) -> None:
        if self.connection_manager.has_connection(peer_address):
            raise Exception("Already connected to: {}".format(peer_address))
        self.peer_client.connect_address(peer_address)

    def connect_peer_async(self, peer_address: PeerAddress) -> None:
        if self.connection_manager.has_connection(peer_address):
            return
        self.peer_client.connect_address_async(peer_address)

    def disconnect_peer(self, peer_address: PeerAddress) -> None:
        self.connection_manager.stop_connection(peer_address)

    def get_connected_peer(self, peer_address: PeerAddress) -> Optional[Peer]:
        return self.connection_manager.get_peer(peer_address)

    def get_connected_peers(self) -> List[Peer]:
        return self.connection_manager.peers

    def broadcast_msg(self, msg: MsgSerializable) -> int:
        """Send a message to all connected peers.

        Returns:
            int: the number of peers message was sent to.
        """
        count = 0
        for peer in self.connection_manager.peers:
            try:
                peer.send_msg(msg)
                count += 1
            except Exception:
                logger.exception("Failed to send msg to peer: {}".format(
                    peer,
                ))
        return count

    def update_local_subscriptions(self, locator: CSqueakLocator) -> None:
        for peer in self.connection_manager.peers:
            try:
                peer.update_local_subscription(locator)
            except Exception:
                logger.exception("Failed to update local subcription with peer: {}".format(
                    peer,
                ))

    @property
    def local_address(self) -> PeerAddress:
        return PeerAddress(
            network=Network.IPV4,
            host=self.local_ip,
            port=self.local_port,
        )

    @property
    def external_address(self) -> PeerAddress:
        return PeerAddress(
            network=Network.IPV4,
            host=self.external_host or self.local_ip,
            port=self.local_port,
        )

    def subscribe_connected_peers(self, stopped) -> Iterable[List[Peer]]:
        # yield from self.connection_manager.yield_peers_changed(stopped)
        for item in self.connection_manager.yield_peers_changed(stopped):
            logger.info("subscribe_connected_peers yielding item: {}".format(
                item,
            ))
            yield item

    def subscribe_connected_peer(self, peer_address: PeerAddress, stopped) -> Iterable[Peer]:
        yield from self.connection_manager.yield_single_peer_changed(
            peer_address,
            stopped,
        )
