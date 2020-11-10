import logging
import threading

from collections import defaultdict

from squeaknode.node.network_task import TimelineNetworkSyncTask
from squeaknode.node.network_task import SingleSqueakNetworkSyncTask
from squeaknode.node.network_sync import NetworkSync

logger = logging.getLogger(__name__)


class SqueakSyncController:
    def __init__(self, blockchain_client, squeak_store, squeak_db, lightning_client):
        self.blockchain_client = blockchain_client
        self.squeak_store = squeak_store
        self.squeak_db = squeak_db
        self.lightning_client = lightning_client
        self.network_sync = NetworkSync(squeak_store, squeak_db, lightning_client)

    def sync_timeline(self):
        try:
            block_info = self.blockchain_client.get_best_block_info()
            block_height = block_info.block_height
        except Exception as e:
            logger.error(
                "Failed to sync because unable to get blockchain info.", exc_info=False
            )
            return
        peers = self.squeak_db.get_peers()
        dowload_timeline_task = TimelineNetworkSyncTask(
            self.network_sync,
            block_height,
        )
        network_sync_result = dowload_timeline_task.sync(peers)
        logger.info("Upload network_sync_result: {}".format(network_sync_result))
        return network_sync_result

    def sync_single_squeak(self, squeak_hash, peers):
        timeline_sync_task = SingleSqueakNetworkSyncTask(
            self.network_sync,
            squeak_hash,
        )
        network_sync_result = timeline_sync_task.sync(peers)
        logger.info("Download single squeak network_sync_result: {}".format(network_sync_result))
        return network_sync_result
