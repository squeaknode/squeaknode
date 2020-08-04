import logging

from squeakserver.server.util import get_hash
from squeakserver.node.squeak_peer_syncer import PeerDownloadTask

logger = logging.getLogger(__name__)


HOUR_IN_SECONDS = 3600


class SqueakSyncStatus:
    def __init__(self):
        pass


class SqueakSyncController:
    def __init__(self, blockchain_client, squeak_store, postgres_db):
        self.squeak_sync_status = SqueakSyncStatus()
        self.blockchain_client = blockchain_client
        self.squeak_store = squeak_store
        self.postgres_db = postgres_db

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
                peer_download_task = PeerDownloadTask(peer, block_height, self.squeak_store, self.postgres_db)
                peer_download_task.download()

    def _upload_to_peers(self, peers, block_height):
        for peer in peers:
            if peer.uploading:
                logger.info("Uploading to peer: {} with current block: {}".format(peer, block_height))
