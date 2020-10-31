import logging
import threading

from squeaknode.network.peer_client import PeerClient
from squeaknode.node.peer_get_offer import PeerGetOffer
from squeaknode.node.peer_download import PeerDownload

logger = logging.getLogger(__name__)


LOOKUP_BLOCK_INTERVAL = 1008  # 1 week


class NetworkSyncTask:
    def __init__(
        self,
        squeak_store,
        postgres_db,
        lightning_client,
    ):
        self.squeak_store = squeak_store
        self.postgres_db = postgres_db
        self.lightning_client = lightning_client

    def sync(self, peers):
        for peer in peers:
            sync_peer_thread = threading.Thread(
                target=self.sync_peer,
                args=(peer,),
            )
            sync_peer_thread.start()

    def sync_peer(self, peer):
        # peer_upload = PeerUpload(
        #     peer,
        #     self.squeak_store,
        #     self.postgres_db,
        #     self.lightning_client,
        # )
        # try:
        #     logger.debug("Trying to upload to peer: {}".format(peer))
        #     with self.UploadingContextManager(
        #         peer, peer_upload, self.squeak_sync_status
        #     ) as uploading_manager:
        #         peer_upload.upload(block_height)
        # except Exception as e:
        #     logger.error("Upload from peer failed.", exc_info=True)
        pass


class TimelineNetworkSyncTask(NetworkSyncTask):
    def __init__(
        self,
        squeak_store,
        postgres_db,
        lightning_client,
        block_height,
    ):
        super().__init__(squeak_store, postgres_db, lightning_client)
        self.block_height = block_height

    def sync_peer(self, peer):
        if not peer.downloading:
            return
        peer_download = PeerDownload(
            peer,
            self.squeak_store,
            self.postgres_db,
            self.lightning_client,
        )
        try:
            logger.debug("Trying to download from peer: {}".format(peer))
            peer_download.download(self.block_height)
        except Exception as e:
            logger.error("Download from peer failed.", exc_info=True)
