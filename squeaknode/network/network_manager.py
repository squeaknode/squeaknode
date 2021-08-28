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
from typing import List
from typing import Optional

import squeak.params
from squeak.messages import MsgSerializable

from squeaknode.core.peer_address import PeerAddress
from squeaknode.network.connection import Connection
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
        self.local_ip = socket.gethostbyname('localhost')
        self.local_port = self.config.server.rpc_port or squeak.params.params.DEFAULT_PORT
        self.peer_server = None
        self.peer_client = None
        self.connection_manager = ConnectionManager()

    def start(self, squeak_controller):
        peer_handler = PeerHandler(
            squeak_controller,
            self.handle_connection,
        )
        self.peer_server = PeerServer(
            peer_handler,
            self.local_port,
        )
        self.peer_client = PeerClient(
            peer_handler,
        )
        self.peer_server.start()

    def stop(self):
        self.peer_server.stop()
        self.connection_manager.stop_all_connections()

    def connect_peer(self, peer_address: PeerAddress) -> None:
        port = peer_address.port or squeak.params.params.DEFAULT_PORT
        peer_address = PeerAddress(
            host=peer_address.host,
            port=port,
        )
        if self.connection_manager.has_connection(peer_address):
            return
        self.peer_client.connect_address(peer_address)

    def disconnect_peer(self, peer_address: PeerAddress) -> None:
        self.connection_manager.stop_connection(peer_address)

    def get_connected_peer(self, peer_address: PeerAddress) -> Optional[Peer]:
        return self.connection_manager.get_peer(peer_address)

    def get_connected_peers(self) -> List[Peer]:
        return self.connection_manager.peers

    def broadcast_msg(self, msg: MsgSerializable) -> None:
        for peer in self.connection_manager.peers:
            try:
                peer.send_msg(msg)
            except Exception:
                logger.exception("Failed to send msg to peer: {}".format(
                    peer,
                ))

    def handle_connection(
            self,
            squeak_controller,
            peer_socket: socket.socket,
            address: PeerAddress,
            outgoing: bool,
    ):
        """Handles all sending and receiving of messages for the given peer.

        This method blocks until the peer connection has stopped.
        """
        peer = Peer(
            peer_socket,
            self.local_address,
            address,
            outgoing,
        )

        logger.debug(
            'Setting up connection for peer address {} ...'.format(address))
        with Connection(peer, squeak_controller).connect(
                self.connection_manager
        ) as connection:
            connection.handle_connection()
        logger.debug('Stopped connection for peer address {}.'.format(address))

    @property
    def local_address(self) -> PeerAddress:
        return PeerAddress(
            self.local_ip,
            self.local_port,
        )

    def subscribe_connected_peers(self, stopped):
        # subscription_client = ConnectedPeersSubscriptionClient(
        #     self.connection_manager,
        #     stopped,
        # )
        for result in self.connection_manager.yield_peers_changed(stopped):
            yield result
