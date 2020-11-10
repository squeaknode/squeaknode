import logging
import threading

logger = logging.getLogger(__name__)


class SqueakPeerSyncWorker:
    def __init__(
        self,
        squeak_sync_controller,
        sync_interval_s,
    ):
        self.squeak_sync_controller = squeak_sync_controller
        self.sync_interval_s = sync_interval_s

    def sync_timeline(self):
        logger.info("Syncing timeline with peers...")
        self.squeak_sync_controller.sync_timeline()

    def start_running(self):
        if self.sync_interval_s:
            threading.Timer(self.sync_interval_s, self.start_running).start()
            self.sync_timeline()
