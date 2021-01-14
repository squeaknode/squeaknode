import logging

from squeaknode.sync.network_task import SingleSqueakDownloadSync
from squeaknode.sync.network_task import SingleSqueakUploadSync
from squeaknode.sync.network_task import TimelineDownloadSync
from squeaknode.sync.network_task import TimelineUploadSync

logger = logging.getLogger(__name__)


class SqueakSyncController:
    def __init__(self, squeak_controller, sync_block_range):
        self.squeak_controller = squeak_controller
        self.sync_block_range = sync_block_range

    def download_timeline(self, block_range=None):
        block_range = block_range or self.sync_block_range
        try:
            block_height = self.squeak_controller.get_best_block_height()
        except Exception:
            logger.error(
                "Failed to download timeline because unable to get best block height.", exc_info=False
            )
            return
        min_block = block_height - block_range
        max_block = block_height
        # dowload_timeline_task = DownloadTimelineSync(
        #     self.squeak_controller,
        #     min_block,
        #     max_block,
        # )
        # dowload_timeline_task.sync()
        TimelineDownloadSync(
            self.squeak_controller,
            min_block,
            max_block,
        ).sync()

    def upload_timeline(self, block_range=None):
        block_range = block_range or self.sync_block_range
        try:
            block_height = self.squeak_controller.get_best_block_height()
        except Exception:
            logger.error(
                "Failed to upload timeline because unable to get best block height.", exc_info=False
            )
            return
        min_block = block_height - block_range
        max_block = block_height
        # dowload_timeline_task = DownloadTimelineSync(
        #     self.squeak_controller,
        #     min_block,
        #     max_block,
        # )
        # dowload_timeline_task.sync()
        TimelineUploadSync(
            self.squeak_controller,
            min_block,
            max_block,
        ).sync()

    def download_single_squeak(self, squeak_hash):
        SingleSqueakDownloadSync(
            self.squeak_controller,
            squeak_hash,
        ).sync()

    def upload_single_squeak(self, squeak_hash):
        SingleSqueakUploadSync(
            self.squeak_controller,
            squeak_hash,
        ).sync()
