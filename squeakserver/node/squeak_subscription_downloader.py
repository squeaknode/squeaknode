import logging
import queue
import threading

logger = logging.getLogger(__name__)


SUBSCRIBE_UPDATE_INTERVAL_S = 10.0


class SqueakSubscriptionDownloader:
    def __init__(self,
                 postgres_db,
                 squeak_store,
                 blockchain_client,
                 update_interval_s=SUBSCRIBE_UPDATE_INTERVAL_S,
    ):
        self.postgres_db = postgres_db
        self.squeak_store = squeak_store
        self.blockchain_client = blockchain_client
        self.update_interval_s = update_interval_s

    def sync_subscriptions(self):
        logger.info("Syncing subscriptions...")
        subscriptions = self._get_subscriptions()
        for subscription in subscriptions:
            logger.info("Syncing subscription: {}".format(subscription))

    def start_running(self):
        threading.Timer(self.update_interval_s, self.start_running).start()
        self.sync_subscriptions()

    def _get_subscriptions(self):
        return self.postgres_db.get_subscriptions()
