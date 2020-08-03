import logging
import queue
import threading

logger = logging.getLogger(__name__)


SUBSCRIBE_UPDATE_INTERVAL_S = 60.0


class SqueakPeerDownloader:
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

    def sync_peers(self):
        logger.info("Syncing peers...")
        peers = self._get_peers()

        try:
            block_info = self.blockchain_client.get_best_block_info()
            block_height = block_info.block_height
        except Exception as e:
            logger.error("Failed to sync because unable to get blockchain info.", exc_info=True)
            return

        for peer in peers:
            if peer.downloading:
                logger.info("Syncing peer: {} with current block: {}".format(peer, block_height))

    def start_running(self):
        threading.Timer(self.update_interval_s, self.start_running).start()
        self.sync_peers()

    def _get_peers(self):
        return self.postgres_db.get_peers()
