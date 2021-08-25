import logging
import socket
import threading

from squeaknode.core.peer_address import PeerAddress


logger = logging.getLogger(__name__)


class PeerHandler():
    """Handles new peer connection.
    """

    def __init__(
            self,
            squeak_controller,
            handle_connection_fn,
    ):
        super().__init__()
        self.squeak_controller = squeak_controller
        self.handle_connection_fn = handle_connection_fn

    def handle_connection(self, peer_socket: socket.socket, address: PeerAddress, outgoing: bool):
        threading.Thread(
            target=self.handle_connection_fn,
            args=(self.squeak_controller, peer_socket, address, outgoing,),
        ).start()
