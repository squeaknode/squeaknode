import logging
import threading

from squeakserver.server.util import get_hash
from squeakserver.node.squeak_peer_syncer import PeerDownloadTask

logger = logging.getLogger(__name__)


HOUR_IN_SECONDS = 3600


class SqueakSyncStatus:
    def __init__(self):
        self.downloads = {}
        self.uploads = {}

    def add_download(self, peer, peer_download):
        self.downloads[peer.peer_id] = peer_download

    def is_downloading(self, peer):
        return peer.peer_id in self.downloads

    def remove_download(self, peer):
        del self.downloads[peer.peer_id]

    def get_current_downloads(self):
        self.downloads.keys


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
                self._download_from_peer(peer, block_height)

    def _upload_to_peers(self, peers, block_height):
        for peer in peers:
            if peer.uploading:
                logger.info("Uploading to peer: {} with current block: {}".format(peer, block_height))

    def _download_from_peer(self, peer, block_height):
        peer_download_task = PeerDownloadTask(
            peer,
            block_height,
            self.squeak_store,
            self.postgres_db,
            self.squeak_sync_status,
        )
        peer_download_task.download()
        try:
            logger.info("Trying to download from peer: {}".format(peer))
            with self.DownloadingContextManager(peer, peer_download_task, self.squeak_sync_status) as downloading_manager:
                download_thread = threading.Thread(target=peer_download_task.download)
                download_thread.start()
        except Exception as e:
            logger.error("Download from peer failed.", exc_info=True)

    class DownloadingContextManager():
        def __init__(self, peer, peer_download, squeak_sync_status):
            logger.info('init method called')
            self.peer = peer
            self.peer_download = peer_download
            self.squeak_sync_status = squeak_sync_status

            if self.squeak_sync_status.is_downloading(self.peer):
                raise Exception("Peer is already downloading: {}".format(self.peer))

        def __enter__(self):
            logger.info('enter method called')
            self.squeak_sync_status.add_download(self.peer, self.peer_download)
            logger.info('current downloads: {}'.format(self.squeak_sync_status.get_current_downloads()))
            return self

        def __exit__(self, exc_type, exc_value, exc_traceback):
            logger.info('exit method called')
            self.squeak_sync_status.remove_download(self.peer)
