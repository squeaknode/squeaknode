import logging

from squeaknode.sync.network_sync import SingleSqueakDownloadSync
from squeaknode.sync.network_sync import SingleSqueakUploadSync
from squeaknode.sync.network_sync import TimelineDownloadSync
from squeaknode.sync.network_sync import TimelineUploadSync

logger = logging.getLogger(__name__)


class SqueakSyncController:

    def __init__(self, squeak_controller, sync_block_range):
        self.squeak_controller = squeak_controller
        self.sync_block_range = sync_block_range

    def download_timeline(self, block_range=None, timeout_s=None):
        TimelineDownloadSync(
            self.squeak_controller,
            timeout_s,
            block_range,
        ).sync()

    def upload_timeline(self, timeout_s=None):
        TimelineUploadSync(
            self.squeak_controller,
            timeout_s,
        ).sync()

    def download_single_squeak(self, squeak_hash, timeout_s=None):
        SingleSqueakDownloadSync(
            self.squeak_controller,
            timeout_s,
            squeak_hash,
        ).sync()

    def upload_single_squeak(self, squeak_hash, timeout_s=None):
        SingleSqueakUploadSync(
            self.squeak_controller,
            timeout_s,
            squeak_hash,
        ).sync()
