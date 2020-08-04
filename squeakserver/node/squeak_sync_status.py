import logging
import threading

from squeakserver.server.util import get_hash
from squeakserver.node.peer_download import PeerDownload
from squeakserver.node.peer_upload import PeerUpload

logger = logging.getLogger(__name__)


HOUR_IN_SECONDS = 3600


class SqueakSyncStatus:
    def __init__(self):
        self.downloads = {}
        self.uploads = {}

    def add_download(self, peer, peer_download):
        self.downloads[peer.peer_id] = peer_download

    def add_upload(self, peer, peer_upload):
        self.uploads[peer.peer_id] = peer_upload

    def is_downloading(self, peer):
        return peer.peer_id in self.downloads

    def is_uploading(self, peer):
        return peer.peer_id in self.uploads

    def remove_download(self, peer):
        del self.downloads[peer.peer_id]

    def remove_upload(self, peer):
        del self.uploads[peer.peer_id]

    def get_current_downloads(self):
        return self.downloads.values()

    def get_current_uploads(self):
        return self.uploads.values()


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
        self._upload_to_peers(peers, block_height)

    def _download_from_peers(self, peers, block_height):
        for peer in peers:
            if peer.downloading:
                self._download_from_peer(peer, block_height)

    def _upload_to_peers(self, peers, block_height):
        for peer in peers:
            if peer.uploading:
                self._upload_to_peer(peer, block_height)

    def _download_from_peer(self, peer, block_height):
        peer_download = PeerDownload(
            peer,
            block_height,
            self.squeak_store,
            self.postgres_db,
        )
        try:
            logger.info("Trying to download from peer: {}".format(peer))
            with self.DownloadingContextManager(peer, peer_download, self.squeak_sync_status) as downloading_manager:
                download_thread = threading.Thread(target=peer_download.download)
                download_thread.start()
        except Exception as e:
            logger.error("Download from peer failed.", exc_info=True)

    def _upload_to_peer(self, peer, block_height):
        peer_upload = PeerUpload(
            peer,
            block_height,
            self.squeak_store,
            self.postgres_db,
        )
        try:
            logger.info("Trying to upload to peer: {}".format(peer))
            with self.UploadingContextManager(peer, peer_upload, self.squeak_sync_status) as uploading_manager:
                upload_thread = threading.Thread(target=peer_upload.upload)
                upload_thread.start()
        except Exception as e:
            logger.error("Upload from peer failed.", exc_info=True)

    class DownloadingContextManager():
        def __init__(self, peer, peer_download, squeak_sync_status):
            logger.info('download init method called')
            self.peer = peer
            self.peer_download = peer_download
            self.squeak_sync_status = squeak_sync_status

            if self.squeak_sync_status.is_downloading(self.peer):
                raise Exception("Peer is already downloading: {}".format(self.peer))

        def __enter__(self):
            logger.info('download enter method called')
            self.squeak_sync_status.add_download(self.peer, self.peer_download)
            logger.info('current downloads: {}'.format(self.squeak_sync_status.get_current_downloads()))
            logger.info('is downloading: {}'.format(self.squeak_sync_status.is_downloading(self.peer)))
            return self

        def __exit__(self, exc_type, exc_value, exc_traceback):
            logger.info('exit method called')
            self.squeak_sync_status.remove_download(self.peer)

    class UploadingContextManager():
        def __init__(self, peer, peer_upload, squeak_sync_status):
            logger.info('upload init method called')
            self.peer = peer
            self.peer_upload = peer_upload
            self.squeak_sync_status = squeak_sync_status

            if self.squeak_sync_status.is_uploading(self.peer):
                raise Exception("Peer is already uploading: {}".format(self.peer))

        def __enter__(self):
            logger.info('upload enter method called')
            self.squeak_sync_status.add_upload(self.peer, self.peer_upload)
            logger.info('current uploads: {}'.format(self.squeak_sync_status.get_current_uploads()))
            return self

        def __exit__(self, exc_type, exc_value, exc_traceback):
            logger.info('exit method called')
            self.squeak_sync_status.remove_upload(self.peer)
