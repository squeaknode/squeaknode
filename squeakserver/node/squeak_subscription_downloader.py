import logging
import queue
import threading

logger = logging.getLogger(__name__)


SUBSCRIBE_UPDATE_INTERVAL_S = 10.0


class SqueakSubscriptionDownloader:
    def __init__(self, postgres_db, squeak_store, update_interval_s=SUBSCRIBE_UPDATE_INTERVAL_S):
        self.postgres_db = postgres_db
        self.squeak_store = squeak_store
        self.update_interval_s = update_interval_s

    def sync_subscriptions(self):
        logger.info("Syncing subscriptions...")

    def start_running(self):
        threading.Timer(self.update_interval_s, self.start_running).start()
        self.sync_subscriptions()
