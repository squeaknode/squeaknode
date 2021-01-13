import logging

from squeaknode.sync.network_task import SingleSqueakNetworkSyncTask
from squeaknode.sync.network_task import TimelineNetworkSyncTask

logger = logging.getLogger(__name__)


class SqueakSyncController:
    def __init__(self, squeak_controller):
        self.squeak_controller = squeak_controller

    def sync_timeline(self, block_range):
        try:
            block_height = self.squeak_controller.get_best_block_height()
        except Exception:
            logger.error(
                "Failed to sync timeline because unable to get best block height.", exc_info=False
            )
            return
        min_block = block_height - block_range
        max_block = block_height
        dowload_timeline_task = TimelineNetworkSyncTask(
            self.squeak_controller,
            min_block,
            max_block,
        )
        network_sync_result = dowload_timeline_task.sync()
        logger.info("Upload network_sync_result: {}".format(
            network_sync_result))
        return network_sync_result

    def sync_single_squeak(self, squeak_hash):
        timeline_sync_task = SingleSqueakNetworkSyncTask(
            self.squeak_controller,
            squeak_hash,
        )
        network_sync_result = timeline_sync_task.sync()
        logger.info(
            "Download single squeak network_sync_result: {}".format(
                network_sync_result)
        )
        return network_sync_result
