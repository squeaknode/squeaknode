import logging
import threading

from squeaknode.network.connection_manager import ConnectionManager
from squeaknode.network.peer import Peer
from squeaknode.node.squeak_controller import SqueakController


logger = logging.getLogger(__name__)


class PeerHandler():
    """Handles new peer connection.
    """

    def __init__(
            self,
            squeak_controller: SqueakController,
            connection_manager: ConnectionManager,
    ):
        super().__init__()
        self.squeak_controller = squeak_controller
        self.connection_manager = connection_manager

    def start(self, peer_socket, address, outgoing):
        """Handles all sending and receiving of messages for the given peer.

        This method blocks until the peer connection has stopped.
        """
        if self.connection_manager.has_connection(address):
            return

        logger.debug(
            'Setting up controller for peer address {} ...'.format(address))
        with Peer(peer_socket, address, outgoing).open_connection(self.squeak_controller) as peer:
            self.connection_manager.add_peer(peer)
            peer.handle_messages(self.squeak_controller)
        self.connection_manager.remove_peer(peer)
        logger.debug('Stopped controller for peer address {}.'.format(address))

    def handle_connection(self, peer_socket, address, outgoing):
        threading.Thread(
            target=self.start,
            args=(peer_socket, address, outgoing,),
        ).start()


# class PeerListener(PeerMessageHandler):
#     """Handles receiving messages from a peer.
#     """

#     def __init__(self, peer_message_handler) -> None:
#         self.peer_message_handler = peer_message_handler

#     def listen_msgs(self):
#         while True:
#             try:
#                 self.peer_message_handler.handle_msgs()
#             except Exception as e:
#                 logger.exception('Error in handle_msgs: {}'.format(e))
#                 return


# class PeerHandshaker(Connection):
#     """Handles the peer handshake.
#     """

#     def __init__(self, peer, connection_manager, peer_server, squeaks_access) -> None:
#         super().__init__(peer, connection_manager, peer_server, squeaks_access)

#     def hanshake(self):
#         # Initiate handshake with the peer if the connection is outgoing.
#         if self.peer.outgoing:
#             self.initiate_handshake()

#         # Sleep for 10 seconds.
#         time.sleep(10)

#         # Disconnect from peer if handshake is not complete.
#         if self.peer.has_handshake_timeout():
#             logger.info('Closing peer because of handshake timeout {}'.format(self.peer))
#             self.peer.close()


# class PeerPingChecker():
#     """Handles receiving messages from a peer.
#     """

#     def __init__(self, peer_message_handler) -> None:
#         super().__init__()
#         self.peer_message_handler = peer_message_handler

#     def handle_msgs(self):
#         while True:
#             try:
#                 self.peer_message_handler.handle_msgs()
#             except Exception as e:
#                 logger.exception('Error in handle_msgs: {}'.format(e))
#                 return
