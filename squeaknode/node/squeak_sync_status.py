import logging

from squeaknode.node.network_sync import NetworkSync
from squeaknode.node.network_task import SingleSqueakNetworkSyncTask
from squeaknode.node.network_task import TimelineNetworkSyncTask

logger = logging.getLogger(__name__)


LOOKUP_BLOCK_INTERVAL = 1008  # 1 week


class SqueakSyncController:
    def __init__(self, blockchain_client, squeak_store, squeak_db, lightning_client):
        self.blockchain_client = blockchain_client
        self.squeak_store = squeak_store
        self.squeak_db = squeak_db
        self.lightning_client = lightning_client
        self.network_sync = NetworkSync(
            squeak_store, squeak_db, lightning_client)

    def sync_timeline(self):
        try:
            block_info = self.blockchain_client.get_best_block_info()
            block_height = block_info.block_height
        except Exception:
            logger.error(
                "Failed to sync because unable to get blockchain info.", exc_info=False
            )
            return
        min_block = block_height - LOOKUP_BLOCK_INTERVAL
        max_block = block_height
        peers = self.squeak_db.get_peers()
        dowload_timeline_task = TimelineNetworkSyncTask(
            self.network_sync,
            min_block,
            max_block,
        )
        network_sync_result = dowload_timeline_task.sync(peers)
        logger.info("Upload network_sync_result: {}".format(
            network_sync_result))
        return network_sync_result

    def sync_single_squeak(self, squeak_hash, peers):
        timeline_sync_task = SingleSqueakNetworkSyncTask(
            self.network_sync,
            squeak_hash,
        )
        network_sync_result = timeline_sync_task.sync(peers)
        logger.info(
            "Download single squeak network_sync_result: {}".format(
                network_sync_result)
        )
        return network_sync_result
