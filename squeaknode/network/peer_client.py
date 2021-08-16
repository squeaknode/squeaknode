import logging
import socket
import threading


MIN_PEERS = 5
MAX_PEERS = 10
UPDATE_THREAD_SLEEP_TIME = 10


logger = logging.getLogger(__name__)


class PeerClient(object):
    """Creates outgoing connections to other peers in the network.
    """

    def __init__(self, peer_handler):
        self.peer_handler = peer_handler

    def make_connection(self, address):
        logger.debug('Making connection to {}'.format(address))
        logger.info('Making connection to {}'.format(address))
        try:
            peer_socket = socket.socket()
            logger.info('Got socket to {}'.format(address))
            peer_socket.connect(address)
            peer_socket.setblocking(True)
            self.peer_handler.handle_connection(
                peer_socket, address, outgoing=True)
        except Exception:
            logger.exception('Failed to make connection to {}'.format(address))

    def connect_address(self, address):
        """Connect to new address."""
        logger.debug('Connecting to peer with address {}'.format(address))
        logger.info('Connecting to peer with address {}'.format(address))
        threading.Thread(
            target=self.make_connection,
            args=(address,),
            name="peer_client_connection_thread",
        ).start()
