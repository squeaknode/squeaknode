import logging
import queue
import threading
from dataclasses import dataclass
from typing import Any, List

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
        logger.debug(
            "Network sync for class {}".format(
                self.__class__,
            )
        )
        run_sync_thread = threading.Thread(
            target=self._run_sync,
            args=(peers,),
        )
        run_sync_thread.start()
        remaining_peer_ids = set(peer.peer_id for peer in peers)
        completed_peer_ids = set()
        failed_peer_ids = set()

        while len(remaining_peer_ids) > 0:
            item = self.queue.get()
            logger.info(f"Working on {item}")
            if item.completed_peer_id:
                completed_peer_ids.add(item.completed_peer_id)
                remaining_peer_ids.remove(item.completed_peer_id)
            if item.failed_peer_id:
                failed_peer_ids.add(item.failed_peer_id)
                remaining_peer_ids.remove(item.failed_peer_id)
            logger.info(f"Finished {item}")
            self.queue.task_done()

        logger.info("Returning from sync...")
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
        except Exception:
            logger.error("Sync with peer failed.", exc_info=True)
            self.queue.put(PeerSyncResult(failed_peer_id=peer.peer_id))


class TimelineNetworkSyncTask(NetworkSyncTask):
    def __init__(
        self,
        network_sync,
        min_block,
        max_block,
    ):
        super().__init__(network_sync)
        self.min_block = min_block
        self.max_block = max_block

    def sync_peer(self, peer):
        self.network_sync.sync_timeline(peer, self.min_block, self.max_block)


class SingleSqueakNetworkSyncTask(NetworkSyncTask):
    def __init__(
        self,
        network_sync,
        squeak_hash,
    ):
        super().__init__(network_sync)
        self.squeak_hash = squeak_hash

    def sync_peer(self, peer):
        self.network_sync.sync_single_squeak(peer, self.squeak_hash)
