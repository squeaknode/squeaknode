import logging

from squeaknode.node.peer_connection import PeerConnection
from squeaknode.node.peer_task import PeerSyncTask

logger = logging.getLogger(__name__)


class NetworkSync:
    def __init__(
        self,
        squeak_store,
        squeak_db,
        lightning_client,
    ):
        self.squeak_store = squeak_store
        self.squeak_db = squeak_db
        self.lightning_client = lightning_client

    def sync_timeline(self, peer, min_block, max_block):
        if not peer.downloading:
            return
        peer_connection = PeerConnection(peer)
        peer_sync_task = PeerSyncTask(
            peer_connection,
            self.squeak_store,
            self.squeak_db,
            self.lightning_client,
        )
        if peer.uploading:
            peer_sync_task.upload(min_block, max_block)
        if peer.downloading:
            peer_sync_task.download(min_block, max_block)

    def sync_single_squeak(self, peer, squeak_hash):
        if not peer.downloading:
            return
        peer_connection = PeerConnection(peer)
        peer_sync_task = PeerSyncTask(
            peer_connection,
            self.squeak_store,
            self.squeak_db,
            self.lightning_client,
        )
        if peer.uploading:
            peer_sync_task.upload_single_squeak(squeak_hash)
        if peer.downloading:
            peer_sync_task.download_single_squeak(squeak_hash)
