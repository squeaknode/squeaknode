import logging
import threading

from squeaknode.node.squeak_controller import SqueakController

logger = logging.getLogger(__name__)


class SqueakPeerSyncWorker:
    def __init__(
        self,
        squeak_controller: SqueakController,
        sync_interval_s,
    ):
        self.squeak_controller = squeak_controller
        self.sync_interval_s = sync_interval_s

    def sync_timeline(self):
        logger.info("Syncing timeline with peers...")
        # self.print_running_threads()
        self.squeak_controller.sync_timeline()
        self.squeak_controller.share_squeaks()

    def start_running(self):
        if self.sync_interval_s:
            timer = threading.Timer(
                self.sync_interval_s,
                self.start_running,
            )
            timer.daemon = True
            timer.name = "squeak_peer_sync_thread"
            timer.start()
            self.sync_timeline()

    # def print_running_threads(self):
    #     for thread in threading.enumerate():
    #         print(thread.name)
