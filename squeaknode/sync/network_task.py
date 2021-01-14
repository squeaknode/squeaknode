import logging
import threading
from abc import ABC
from abc import abstractmethod

from squeaknode.sync.peer_task import PeerSyncTask

logger = logging.getLogger(__name__)


# class PeerSyncResult(NamedTuple):
#     completed_peer_id: Any = None
#     failed_peer_id: Any = None
#     timeout: Any = None


# class NetworkSyncResult(NamedTuple):
#     completed_peer_ids: List[int]
#     failed_peer_ids: List[int]
#     timeout_peer_ids: List[int]


# class NetworkSyncTask:
#     def __init__(
#         self,
#         squeak_controller,
#     ):
#         self.squeak_controller = squeak_controller
#         self.queue = queue.Queue()

#     def sync(self):
#         peers = self.squeak_controller.get_peers()
#         logger.debug(
#             "Network sync for class {} with peers: {}".format(
#                 self.__class__,
#                 peers,
#             )
#         )
#         run_sync_thread = threading.Thread(
#             target=self._run_sync,
#             args=(peers,),
#         )
#         run_sync_thread.start()
#         remaining_peer_ids = set(peer.peer_id for peer in peers)
#         completed_peer_ids = set()
#         failed_peer_ids = set()

#         while len(remaining_peer_ids) > 0:
#             item = self.queue.get()
#             logger.debug(f"Working on {item}")
#             if item.completed_peer_id:
#                 completed_peer_ids.add(item.completed_peer_id)
#                 remaining_peer_ids.remove(item.completed_peer_id)
#             if item.failed_peer_id:
#                 failed_peer_ids.add(item.failed_peer_id)
#                 remaining_peer_ids.remove(item.failed_peer_id)
#             logger.debug(f"Finished {item}")
#             self.queue.task_done()

#         logger.info("Finished sync with peers.")
#         return NetworkSyncResult(
#             completed_peer_ids=list(completed_peer_ids),
#             failed_peer_ids=list(failed_peer_ids),
#             timeout_peer_ids=list(remaining_peer_ids),
#         )

#     def _run_sync(self, peers):
#         for peer in peers:
#             sync_peer_thread = threading.Thread(
#                 target=self._sync_peer,
#                 args=(peer,),
#             )
#             sync_peer_thread.start()

#     def sync_peer(self, peer):
#         pass

#     def _sync_peer(self, peer):
#         try:
#             logger.debug("Trying to sync with peer: {}".format(peer.peer_id))
#             self.sync_peer(peer)
#             self.queue.put(PeerSyncResult(completed_peer_id=peer.peer_id))
#             logger.info("Finished sync with peer: {}".format(peer))
#         except Exception:
#             logger.error("Failed Sync with peer: {}.".format(
#                 peer), exc_info=True)
#             self.queue.put(PeerSyncResult(failed_peer_id=peer.peer_id))


# class TimelineNetworkSyncTask(NetworkSyncTask):
#     def __init__(
#         self,
#         squeak_controller,
#         min_block,
#         max_block,
#     ):
#         super().__init__(squeak_controller)
#         self.min_block = min_block
#         self.max_block = max_block

#     def sync_peer(self, peer):
#         network_sync = NetworkSync(
#             self.squeak_controller,
#         )
#         network_sync.sync_timeline(peer, self.min_block, self.max_block)


# class SingleSqueakNetworkSyncTask(NetworkSyncTask):
#     def __init__(
#         self,
#         squeak_controller,
#         squeak_hash: bytes,
#     ):
#         super().__init__(squeak_controller)
#         self.squeak_hash = squeak_hash

#     def sync_peer(self, peer):
#         network_sync = NetworkSync(
#             self.squeak_controller,
#         )
#         network_sync.sync_single_squeak(peer, self.squeak_hash)


class NetworkSync(ABC):

    def __init__(
        self,
        squeak_controller,
    ):
        self.squeak_controller = squeak_controller
        self.stopped = threading.Event()

    @abstractmethod
    def get_peers_to_sync(self):
        pass

    # TODO: Rename peer_sync_task to peer_connection or something.
    @abstractmethod
    def sync_peer(self, peer_sync_task):
        pass

    def stop(self):
        self.stopped.set()

    def sync(self):
        peers = self.squeak_controller.get_peers()
        for peer in peers:
            sync_peer_thread = threading.Thread(
                target=self._sync_peer,
                args=(peer,),
            )
            sync_peer_thread.start()
        # TODO: sleep for timeout and then call self._stop()

    def _sync_peer(self, peer):
        # with PeerConnection(peer) as peer_connection:
        #     self.sync_peer(peer_connection)
        with PeerSyncTask(
                self.squeak_controller,
                peer,
                self.stopped,
        ).open_peer_sync_task() as peer_sync_task:
            # if peer.uploading:
            #     peer_sync_task.upload(min_block, max_block)
            # if peer.downloading:
            #     peer_sync_task.download(min_block, max_block)
            self.sync_peer(peer_sync_task)


class DownloadSync(NetworkSync):

    def get_peers_to_sync(self):
        return self.squeak_controller.get_uploading_peers()

    @abstractmethod
    def sync_peer(self, peer_sync_task):
        pass


class UploadSync(NetworkSync):

    def get_peers_to_sync(self):
        return self.squeak_controller.get_uploading_peers()

    @abstractmethod
    def sync_peer(self, peer_sync_task):
        pass


class TimelineDownloadSync(DownloadSync):

    def __init__(
        self,
        squeak_controller,
        min_block,
        max_block,
    ):
        super().__init__(squeak_controller)
        self.min_block = min_block
        self.max_block = max_block

    def sync_peer(self, peer_sync_task):
        peer_sync_task.download(self.min_block, self.max_block)


class SingleSqueakDownloadSync(DownloadSync):

    def __init__(
        self,
        squeak_controller,
        squeak_hash: bytes,
    ):
        super().__init__(squeak_controller)
        self.squeak_hash = squeak_hash

    def sync_peer(self, peer_sync_task):
        peer_sync_task.download_single_squeak(self.squeak_hash)


class TimelineUploadSync(UploadSync):

    def __init__(
        self,
        squeak_controller,
        min_block,
        max_block,
    ):
        super().__init__(squeak_controller)
        self.min_block = min_block
        self.max_block = max_block

    def sync_peer(self, peer_sync_task):
        peer_sync_task.upload(self.min_block, self.max_block)


class SingleSqueakUploadSync(UploadSync):

    def __init__(
        self,
        squeak_controller,
        squeak_hash: bytes,
    ):
        super().__init__(squeak_controller)
        self.squeak_hash = squeak_hash

    def sync_peer(self, peer_sync_task):
        peer_sync_task.upload_single_squeak(self.squeak_hash)
