import logging
import socket
from typing import List

import squeak.params
from squeak.messages import MsgSerializable

from squeaknode.core.peer_address import PeerAddress
from squeaknode.core.squeak_peer import SqueakPeer
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
            self.config.server.rpc_port,
        )
        self.peer_client = PeerClient(
            peer_handler,
        )
        self.peer_server.start()

    def stop(self):
        self.peer_server.stop()
        self.connection_manager.stop_all_connections()

    def connect_peer(self, host: str, port: int) -> None:
        port = port or squeak.params.params.DEFAULT_PORT
        peer_address = PeerAddress(host=host, port=port)
        self.peer_client.connect_address(peer_address)

    def connect_peers(self, peers: List[SqueakPeer]) -> None:
        connected_peers = self.connection_manager.peers
        connected_peer_addrs = [
            peer.address
            for peer in connected_peers
        ]
        for peer in peers:
            peer_addr = (peer.address.host, peer.address.port)
            if peer_addr not in connected_peer_addrs:
                logger.info("Connect to peer: {}".format(
                    peer,
                ))
                self.peer_client.connect_address(peer.address)

    def disconnect_peer(self, host: str, port: int) -> None:
        peer_address = PeerAddress(host=host, port=port)
        self.connection_manager.stop_connection(peer_address)

    def get_connected_peer(self, host, port):
        address = (host, port)
        return self.connection_manager.get_peer(address)

    def get_connected_peers(self):
        return self.connection_manager.peers

    def broadcast_msg(self, msg: MsgSerializable) -> None:
        for peer in self.connection_manager.peers:
            try:
                peer.send_msg(msg)
            except Exception:
                logger.exception("Failed to send msg to peer: {}".format(
                    peer,
                ))

    def handle_connection(self, squeak_controller, peer_socket, address, outgoing):
        """Handles all sending and receiving of messages for the given peer.

        This method blocks until the peer connection has stopped.
        """
        if self.connection_manager.has_connection(address):
            return

        logger.debug(
            'Setting up controller for peer address {} ...'.format(address))
        with Peer(peer_socket, address, outgoing).open_connection(squeak_controller) as peer:
            self.connection_manager.add_peer(peer)
            try:
                peer.handle_messages(squeak_controller)
            except Exception:
                logger.exception("Handling messages failed.")
            finally:
                self.connection_manager.remove_peer(peer)
        logger.debug('Stopped controller for peer address {}.'.format(address))

    def get_address(self):
        # TODO: Add return type.
        return (self.peer_server.ip, self.peer_server.port)

    def get_remote_address(self, address):
        # TODO: Add return type.
        hostname, port = address
        ip = socket.gethostbyname(hostname)
        return (ip, port)
