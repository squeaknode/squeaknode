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
        network_sync,
    ):
        self.network_sync = network_sync
        self.queue = queue.Queue()

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

        while len(remaining_peer_ids) > 0:
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
        pass

    def _sync_peer(self, peer):
        try:
            logger.debug("Trying to sync with peer: {}".format(peer.peer_id))
            self.sync_peer(peer)
            self.queue.put(PeerSyncResult(completed_peer_id=peer.peer_id))
        except Exception as e:
            logger.error("Sync with peer failed.", exc_info=True)
            self.queue.put(PeerSyncResult(failed_peer_id=peer.peer_id))


class DownloadTimelineNetworkSyncTask(NetworkSyncTask):
    def __init__(
        self,
        network_sync,
        block_height,
    ):
        super().__init__(network_sync)
        self.block_height = block_height

    def sync_peer(self, peer):
        self.network_sync.sync_timeline(peer, self.block_height)


class UploadTimelineNetworkSyncTask(NetworkSyncTask):
    def __init__(
        self,
        network_sync,
        block_height,
    ):
        super().__init__(network_sync)
        self.block_height = block_height

    def sync_peer(self, peer):
        self.network_sync.sync_timeline_upload(peer, self.block_height)


class SingleSqueakNetworkSyncTask(NetworkSyncTask):
    def __init__(
        self,
        network_sync,
        squeak_hash,
    ):
        super().__init__(network_sync)
        self.squeak_hash = squeak_hash

    def sync_peer(self, peer):
        self.network_sync.sync_single_squeak_download(peer, self.squeak_hash)
