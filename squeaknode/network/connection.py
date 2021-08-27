import logging
import threading
from contextlib import contextmanager

from squeaknode.network.peer import Peer

HANDSHAKE_TIMEOUT = 5


logger = logging.getLogger(__name__)


class Connection(object):
    """Handles lifecycle of a connection to a peer.
    """

    def __init__(self, peer: Peer, squeak_controller):
        self.peer = peer
        self.squeak_controller = squeak_controller
        self.stopped = threading.Event()

    @contextmanager
    def connect(self, connection_manager):
        self.start_receiving_msgs()
        self.handshake()
        logger.info("Adding peer.")
        connection_manager.add_peer(self.peer)
        try:
            logger.info("Yielding peer.")
            yield self
        except Exception:
            logger.exception("Peer connection failed.")
        finally:
            logger.info("Removing peer.")
            connection_manager.remove_peer(self.peer)

    def handle_connection(self):
        self.peer.sync(self.squeak_controller)
        self.peer.handle_messages(self.squeak_controller)
        logger.info("Finished handle_connection")

    def start_receiving_msgs(self):
        threading.Thread(
            target=self.peer.recv_msgs,
            args=(),
        ).start()

    def handshake(self):
        timer = HandshakeTimer(
            self.peer.stop,
            str(self),
        )
        timer.start_timer()

        if self.peer.outgoing:
            self.peer.send_version()
        self.peer.receive_version()
        if not self.peer.outgoing:
            self.peer.send_version()

        self.peer.set_connected()
        logger.info("HANDSHAKE COMPLETE-----------")
        timer.stop_timer()


class HandshakeTimer:
    """Stop the peer if handshake is not complete before timeout.
    """

    def __init__(self,
                 stop_fn,
                 peer_name,
                 ):
        self.stop_fn = stop_fn
        self.peer_name = peer_name
        self.timer = None

    def start_timer(self):
        self.timer = threading.Timer(
            HANDSHAKE_TIMEOUT,
            self.stop_peer,
        )
        self.timer.name = "handshake_timere_thread_{}".format(self.peer_name)
        self.timer.start()

    def stop_timer(self):
        logger.debug("Canceling handshake timer.")
        self.timer.cancel()

    def stop_peer(self):
        logger.info("Closing peer from handshake timer.")
        self.stop_fn()
