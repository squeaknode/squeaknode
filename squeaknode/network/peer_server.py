import logging
import socket
import threading

import squeak.params


MIN_PEERS = 5
MAX_PEERS = 10
UPDATE_THREAD_SLEEP_TIME = 10


logger = logging.getLogger(__name__)


class PeerServer(object):
    """Maintains connections to other peers in the network.
    """

    def __init__(self, connection_manager, port=None):
        self.ip = socket.gethostbyname('localhost')
        self.port = port or squeak.params.params.DEFAULT_PORT
        self.connection_manager = connection_manager
        self.listen_socket = socket.socket()

    def start(self, peer_handler):
        self.peer_handler = peer_handler

        # Start Listen thread
        threading.Thread(
            target=self.accept_connections,
            name="peer_server_listen_thread",
        ).start()

    def stop(self):
        # TODO: stop accepting connections thread.
        # TODO: stop every peer in connection manager.
        # pass
        logger.info("Stopping peer server listener thread...")
        self.listen_socket.shutdown(socket.SHUT_RDWR)
        self.listen_socket.close()

    def accept_connections(self):
        try:
            self.listen_socket.bind(('', self.port))
            self.listen_socket.listen()
            while True:
                peer_socket, address = self.listen_socket.accept()
                peer_socket.setblocking(True)
                self.peer_handler.handle_connection(
                    peer_socket, address, outgoing=False)
        except Exception:
            logger.info("Stopped accepting incoming connections.")
