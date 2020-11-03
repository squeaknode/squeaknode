import logging
import threading
import queue

from dataclasses import dataclass
from typing import Any
from typing import List

from collections import namedtuple

from squeaknode.network.peer_client import PeerClient
from squeaknode.node.peer_task import PeerSyncTask
from squeaknode.node.peer_connection import PeerConnection

logger = logging.getLogger(__name__)


LOOKUP_BLOCK_INTERVAL = 1008  # 1 week


@dataclass
class PeerSyncResult:
    completed_peer_id: Any = None
    failed_peer_id: Any = None
    timeout: Any = None


@dataclass
class NetworkSyncResult:
    completed_peer_ids: List[int]
    failed_peer_ids: List[int]
    timeout_peer_ids: List[int]


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
        self.queue = queue.Queue()
        #self.in_progress_peers = dict()

    def sync(self, peers):
        logger.debug("Network sync for class {}".format(
            self.__class__,
        ))
        run_sync_thread = threading.Thread(
            target=self._run_sync,
            args=(peers,),
        )
        run_sync_thread.start()
        count = len(peers)
        logger.info(f'Current count {count}')
        remaining_peer_ids = set(peer.peer_id for peer in peers)
        completed_peer_ids = set()
        failed_peer_ids = set()
        while True:
            item = self.queue.get()
            logger.info(f'Working on {item}')
            count -= 1
            if item.completed_peer_id:
                completed_peer_ids.add(item.completed_peer_id)
                remaining_peer_ids.remove(item.completed_peer_id)
            if item.failed_peer_id:
                failed_peer_ids.add(item.failed_peer_id)
                remaining_peer_ids.remove(item.failed_peer_id)
            logger.info(f'Finished {item}')
            logger.info(f'Current count {count}')
            self.queue.task_done()
            if len(remaining_peer_ids) == 0:
                logger.info(f'Returning from sync...')
                return NetworkSyncResult(
                    completed_peer_ids=list(completed_peer_ids),
                    failed_peer_ids=list(failed_peer_ids),
                    timeout_peer_ids=list(remaining_peer_ids),
                )

    def _run_sync(self, peers):
        for peer in peers:
            sync_peer_thread = threading.Thread(
                target=self._sync_peer,
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

    def _sync_peer(self, peer):
        try:
            logger.debug("Trying to sync with peer: {}".format(peer.peer_id))
            self.sync_peer(peer)
            # self.queue.put("Finished sync with peer: {}".format(peer.peer_id))
            self.queue.put(PeerSyncResult(completed_peer_id=peer.peer_id))
        except Exception as e:
            logger.error("Sync with peer failed.", exc_info=True)
            # self.queue.put("Error while syncing from peer: {}".format(peer.peer_id))
            self.queue.put(PeerSyncResult(failed_peer_id=peer.peer_id))


class DownloadTimelineNetworkSyncTask(NetworkSyncTask):
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
        peer_connection = PeerConnection(peer)
        peer_sync_task = PeerSyncTask(
            peer_connection,
            self.squeak_store,
            self.postgres_db,
            self.lightning_client,
        )
        peer_sync_task.download(self.block_height)


class UploadTimelineNetworkSyncTask(NetworkSyncTask):
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
        if not peer.uploading:
            return
        peer_connection = PeerConnection(peer)
        peer_sync_task = PeerSyncTask(
            peer_connection,
            self.squeak_store,
            self.postgres_db,
            self.lightning_client,
        )
        peer_sync_task.upload(self.block_height)


class SingleSqueakNetworkSyncTask(NetworkSyncTask):
    def __init__(
        self,
        squeak_store,
        postgres_db,
        lightning_client,
        squeak_hash,
    ):
        super().__init__(squeak_store, postgres_db, lightning_client)
        self.squeak_hash = squeak_hash

    def sync_peer(self, peer):
        if not peer.downloading:
            return
        peer_connection = PeerConnection(peer)
        peer_sync_task = PeerSyncTask(
            peer_connection,
            self.squeak_store,
            self.postgres_db,
            self.lightning_client,
        )
        peer_sync_task.download_single_squeak(self.squeak_hash)
