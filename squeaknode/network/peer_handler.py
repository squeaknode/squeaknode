import logging
import threading


logger = logging.getLogger(__name__)


class PeerHandler():
    """Handles new peer connection.
    """

    def __init__(
            self,
            squeak_controller,
            network_manager,
    ):
        super().__init__()
        self.squeak_controller = squeak_controller
        self.network_manager = network_manager

    def handle_connection(self, peer_socket, address, outgoing):
        threading.Thread(
            target=self.network_manager.handle_connection,
            args=(self.squeak_controller, peer_socket, address, outgoing,),
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
