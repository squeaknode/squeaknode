import logging

from squeakserver.server.util import get_hash

logger = logging.getLogger(__name__)


HOUR_IN_SECONDS = 3600


class SqueakSyncStatus:
    def __init__(self):
        pass


class SqueakSyncController:
    def __init__(self, blockchain_client, squeak_store):
        self.squeak_sync_status = SqueakSyncStatus()
        self.blockchain_client = blockchain_client
        self.squeak_store = squeak_store

    def sync_peers(self, peers):
        try:
            block_info = self.blockchain_client.get_best_block_info()
            block_height = block_info.block_height
        except Exception as e:
            logger.error("Failed to sync because unable to get blockchain info.", exc_info=True)
            return
        self._download_from_peers(peers, block_height)

    def _download_from_peers(self, peers, block_height):
        for peer in peers:
            if peer.downloading:
                logger.info("Downloading from peer: {} with current block: {}".format(peer, block_height))

    def _upload_to_peers(self, peers, block_height):
        for peer in peers:
            if peer.uploading:
                logger.info("Uploading to peer: {} with current block: {}".format(peer, block_height))
