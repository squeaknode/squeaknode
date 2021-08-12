import logging
import threading

from squeaknode.node.squeak_controller import SqueakController

logger = logging.getLogger(__name__)


class PeerConnectionWorker:
    def __init__(
        self,
        squeak_controller: SqueakController,
        connect_interval_s: int,
    ):
        self.squeak_controller = squeak_controller
        self.connect_interval_s = connect_interval_s

    def connect_peers(self):
        logger.debug("Connecting peers...")
        self.squeak_controller.connect_peers()

    def start_running(self):
        if self.connect_interval_s:
            timer = threading.Timer(
                self.connect_interval_s,
                self.start_running,
            )
            timer.daemon = True
            timer.start()
            self.connect_peers()
