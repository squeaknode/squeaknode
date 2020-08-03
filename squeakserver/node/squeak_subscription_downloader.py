import logging
import queue
import threading

logger = logging.getLogger(__name__)


SUBSCRIBE_UPDATE_INTERVAL_S = 60.0


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

        try:
            block_info = self.blockchain_client.get_best_block_info()
            block_height = block_info.block_height
        except Exception as e:
            logger.error("Failed to sync because unable to get blockchain info.", exc_info=True)
            return

        for subscription in subscriptions:
            if subscription.subscribed:
                logger.info("Syncing subscription: {} with current block: {}".format(subscription, block_height))

    def start_running(self):
        threading.Timer(self.update_interval_s, self.start_running).start()
        self.sync_subscriptions()

    def _get_subscriptions(self):
        return self.postgres_db.get_subscriptions()
