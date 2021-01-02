import logging

from squeaknode.sync.network_sync import NetworkSync
from squeaknode.sync.network_task import SingleSqueakNetworkSyncTask
from squeaknode.sync.network_task import TimelineNetworkSyncTask

logger = logging.getLogger(__name__)


LOOKUP_BLOCK_INTERVAL = 1008  # 1 week


class SqueakSyncController:
    def __init__(self, squeak_controller):
        self.squeak_controller = squeak_controller
        self.network_sync = NetworkSync(
            squeak_controller,
        )

    def sync_timeline(self):
        try:
            block_info = self.squeak_controller.blockchain_client.get_best_block_info()
            block_height = block_info.block_height
        except Exception as e:
            logger.error(
                "Failed to sync because unable to get blockchain info.", exc_info=False
            )
            logger.error("Error e: {}".format(e))
            return
        min_block = block_height - LOOKUP_BLOCK_INTERVAL
        max_block = block_height
        peers = self.squeak_controller.squeak_db.get_peers()
        dowload_timeline_task = TimelineNetworkSyncTask(
            self.network_sync,
            min_block,
            max_block,
        )
        network_sync_result = dowload_timeline_task.sync(peers)
        logger.info("Upload network_sync_result: {}".format(
            network_sync_result))
        return network_sync_result

    def sync_single_squeak(self, squeak_hash):
        peers = self.squeak_controller.squeak_db.get_peers()
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
