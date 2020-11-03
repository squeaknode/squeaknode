import logging
import threading

logger = logging.getLogger(__name__)


SUBSCRIBE_UPDATE_INTERVAL_S = 10.0


class SqueakPeerSyncWorker:
    def __init__(
        self,
        squeak_sync_controller,
        update_interval_s=SUBSCRIBE_UPDATE_INTERVAL_S,
    ):
        self.squeak_sync_controller = squeak_sync_controller
        self.update_interval_s = update_interval_s

    def sync_timeline(self):
        logger.info("Syncing timeline with peers...")
        self.squeak_sync_controller.sync_timeline()

    def start_running(self):
        threading.Timer(self.update_interval_s, self.start_running).start()
        self.sync_timeline()
