import logging
import threading

from collections import defaultdict

from squeaknode.node.peer_download import PeerDownload
from squeaknode.node.peer_single_squeak_download import PeerSingleSqueakDownload
from squeaknode.node.peer_upload import PeerUpload
from squeaknode.node.network_task import TimelineNetworkSyncTask
from squeaknode.node.network_task import SingleSqueakNetworkSyncTask

logger = logging.getLogger(__name__)


HOUR_IN_SECONDS = 3600


class SqueakSyncStatus:
    def __init__(self):
        self.downloads = {}
        self.uploads = {}
        self.single_squeak_downloads = defaultdict(dict)

    def add_download(self, peer, peer_download):
        self.downloads[peer.peer_id] = peer_download

    def add_upload(self, peer, peer_upload):
        self.uploads[peer.peer_id] = peer_upload

    def add_single_squeak_download(self, squeak_hash, peer, peer_download):
        self.single_squeak_downloads[squeak_hash][peer.peer_id] = peer_download

    def is_downloading(self, peer):
        return peer.peer_id in self.downloads

    def is_uploading(self, peer):
        return peer.peer_id in self.uploads

    def is_downloading_single_squeak(self, squeak_hash, peer):
        return peer.peer_id in self.single_squeak_downloads[squeak_hash]

    def remove_download(self, peer):
        del self.downloads[peer.peer_id]

    def remove_upload(self, peer):
        del self.uploads[peer.peer_id]

    def remove_single_peer_download(self, squeak_hash, peer):
        del self.single_squeak_downloads[squeak_hash][peer.peer_id]

    def get_current_downloads(self):
        return self.downloads.values()

    def get_current_uploads(self):
        return self.uploads.values()


class SqueakSyncController:
    def __init__(self, blockchain_client, squeak_store, postgres_db, lightning_client):
        self.squeak_sync_status = SqueakSyncStatus()
        self.blockchain_client = blockchain_client
        self.squeak_store = squeak_store
        self.postgres_db = postgres_db
        self.lightning_client = lightning_client

    def sync_peers(self, peers):
        try:
            block_info = self.blockchain_client.get_best_block_info()
            block_height = block_info.block_height
        except Exception as e:
            logger.error(
                "Failed to sync because unable to get blockchain info.", exc_info=False
            )
            return
        #self._download_from_peers(peers, block_height)
        #self._upload_to_peers(peers, block_height)
        timeline_sync_task = TimelineNetworkSyncTask(
            self.squeak_store,
            self.postgres_db,
            self.lightning_client,
            block_height,
        )
        timeline_sync_task.sync(peers)

    def download_single_squeak_from_peers(self, squeak_hash, peers):
        # for peer in peers:
        #     if peer.downloading:
        #         download_thread = threading.Thread(
        #             target=self._download_single_squeak_from_peer,
        #             args=(
        #                 squeak_hash,
        #                 peer,
        #             ),
        #         )
        #         download_thread.start()
        timeline_sync_task = SingleSqueakNetworkSyncTask(
            self.squeak_store,
            self.postgres_db,
            self.lightning_client,
            squeak_hash,
        )
        timeline_sync_task.sync(peers)


    # def _download_from_peers(self, peers, block_height):
    #     for peer in peers:
    #         if peer.downloading:
    #             download_thread = threading.Thread(
    #                 target=self._download_from_peer,
    #                 args=(
    #                     peer,
    #                     block_height,
    #                 ),
    #             )
    #             download_thread.start()

    # def _upload_to_peers(self, peers, block_height):
    #     for peer in peers:
    #         if peer.uploading:
    #             upload_thread = threading.Thread(
    #                 target=self._upload_to_peer,
    #                 args=(
    #                     peer,
    #                     block_height,
    #                 ),
    #             )
    #             upload_thread.start()

    # def _download_from_peer(self, peer, block_height):
    #     peer_download = PeerDownload(
    #         peer,
    #         self.squeak_store,
    #         self.postgres_db,
    #         self.lightning_client,
    #     )
    #     try:
    #         logger.debug("Trying to download from peer: {}".format(peer))
    #         with self.DownloadingContextManager(
    #             peer, peer_download, self.squeak_sync_status
    #         ) as downloading_manager:
    #             peer_download.download(block_height)
    #     except Exception as e:
    #         logger.error("Download from peer failed.", exc_info=True)

    def _upload_to_peer(self, peer, block_height):
        peer_upload = PeerUpload(
            peer,
            self.squeak_store,
            self.postgres_db,
            self.lightning_client,
        )
        try:
            logger.debug("Trying to upload to peer: {}".format(peer))
            with self.UploadingContextManager(
                peer, peer_upload, self.squeak_sync_status
            ) as uploading_manager:
                peer_upload.upload(block_height)
        except Exception as e:
            logger.error("Upload from peer failed.", exc_info=True)

    # def _download_single_squeak_from_peer(self, squeak_hash, peer):
    #     peer_download = PeerSingleSqueakDownload(
    #         peer,
    #         self.squeak_store,
    #         self.postgres_db,
    #         self.lightning_client,
    #     )
    #     try:
    #         logger.debug("Trying to download single squeak {} from peer: {}".format(squeak_hash, peer))
    #         with self.SingleSqueakDownloadingContextManager(
    #             squeak_hash, peer, peer_download, self.squeak_sync_status
    #         ) as downloading_manager:
    #             peer_download.download_single_squeak(squeak_hash)
    #     except Exception as e:
    #         logger.error("Download single squeak from peer failed.", exc_info=True)

    # class DownloadingContextManager:
    #     def __init__(self, peer, peer_download, squeak_sync_status):
    #         self.peer = peer
    #         self.peer_download = peer_download
    #         self.squeak_sync_status = squeak_sync_status

    #         if self.squeak_sync_status.is_downloading(self.peer):
    #             raise Exception("Peer is already downloading: {}".format(self.peer))

    #     def __enter__(self):
    #         self.squeak_sync_status.add_download(self.peer, self.peer_download)
    #         return self

    #     def __exit__(self, exc_type, exc_value, exc_traceback):
    #         self.squeak_sync_status.remove_download(self.peer)

    # class UploadingContextManager:
    #     def __init__(self, peer, peer_upload, squeak_sync_status):
    #         self.peer = peer
    #         self.peer_upload = peer_upload
    #         self.squeak_sync_status = squeak_sync_status

    #         if self.squeak_sync_status.is_uploading(self.peer):
    #             raise Exception("Peer is already uploading: {}".format(self.peer))

    #     def __enter__(self):
    #         self.squeak_sync_status.add_upload(self.peer, self.peer_upload)
    #         return self

    #     def __exit__(self, exc_type, exc_value, exc_traceback):
    #         self.squeak_sync_status.remove_upload(self.peer)

    # class SingleSqueakDownloadingContextManager:
    #     def __init__(self, squeak_hash, peer, peer_download, squeak_sync_status):
    #         self.squeak_hash = squeak_hash
    #         self.peer = peer
    #         self.peer_download = peer_download
    #         self.squeak_sync_status = squeak_sync_status

    #         if self.squeak_sync_status.is_downloading_single_squeak(self.squeak_hash, self.peer):
    #             raise Exception("Peer {} is already downloading hash: {}".format(self.peer, self.squeak_hash))

    #     def __enter__(self):
    #         self.squeak_sync_status.add_single_squeak_download(self.squeak_hash, self.peer, self.peer_download)
    #         return self

    #     def __exit__(self, exc_type, exc_value, exc_traceback):
    #         self.squeak_sync_status.remove_single_peer_download(self.squeak_hash, self.peer)
