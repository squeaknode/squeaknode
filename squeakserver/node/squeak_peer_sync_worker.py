import logging
import threading

logger = logging.getLogger(__name__)


SUBSCRIBE_UPDATE_INTERVAL_S = 10.0


class SqueakPeerSyncWorker:
    def __init__(
        self,
        postgres_db,
        squeak_sync_controller,
        update_interval_s=SUBSCRIBE_UPDATE_INTERVAL_S,
    ):
        self.postgres_db = postgres_db
        self.squeak_sync_controller = squeak_sync_controller
        self.update_interval_s = update_interval_s

    def sync_peers(self):
        logger.info("Syncing peers...")
        peers = self._get_peers()
        self.squeak_sync_controller.sync_peers(peers)

    def start_running(self):
        threading.Timer(self.update_interval_s, self.start_running).start()
        self.sync_peers()

    def _get_peers(self):
        return self.postgres_db.get_peers()
