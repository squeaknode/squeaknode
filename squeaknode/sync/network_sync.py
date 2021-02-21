import logging
import threading
from abc import ABC
from abc import abstractmethod
from typing import List

from squeaknode.core.squeak_peer import SqueakPeer
from squeaknode.sync.peer_connection import PeerConnection

logger = logging.getLogger(__name__)


class NetworkSync(ABC):

    def __init__(
        self,
        squeak_controller,
        timeout_s,
    ):
        self.squeak_controller = squeak_controller
        self.timeout_s = timeout_s

    @abstractmethod
    def get_peers_to_sync(self) -> List[SqueakPeer]:
        pass

    @abstractmethod
    def sync_peer(self, peer_connection):
        pass

    def sync(self):
        for peer in self.get_peers_to_sync():
            sync_peer_thread = threading.Thread(
                target=self._sync_peer,
                args=(peer,),
            )
            sync_peer_thread.start()

    def _sync_peer(self, peer: SqueakPeer):
        with PeerConnection(
                self.squeak_controller,
                peer.address,
                self.timeout_s,
        ).open_connection() as peer_connection:
            self.sync_peer(peer_connection)


class DownloadSync(NetworkSync):

    def get_peers_to_sync(self):
        return self.squeak_controller.get_downloading_peers()

    @abstractmethod
    def sync_peer(self, peer_connection):
        pass


class UploadSync(NetworkSync):

    def get_peers_to_sync(self):
        return self.squeak_controller.get_uploading_peers()

    @abstractmethod
    def sync_peer(self, peer_connection):
        pass


class TimelineDownloadSync(DownloadSync):

    def __init__(
        self,
        squeak_controller,
        timeout_s,
        block_interval,
    ):
        super().__init__(
            squeak_controller,
            timeout_s,
        )
        self.block_interval = block_interval

    def sync_peer(self, peer_connection):
        peer_connection.download(self.block_interval)


class SingleSqueakDownloadSync(DownloadSync):

    def __init__(
        self,
        squeak_controller,
        timeout_s,
        squeak_hash: bytes,
    ):
        super().__init__(
            squeak_controller,
            timeout_s,
        )
        self.squeak_hash = squeak_hash

    def sync_peer(self, peer_connection):
        peer_connection.download_single_squeak(self.squeak_hash)


class TimelineUploadSync(UploadSync):

    def __init__(
        self,
        squeak_controller,
        timeout_s,
    ):
        super().__init__(
            squeak_controller,
            timeout_s,
        )

    def sync_peer(self, peer_connection):
        peer_connection.upload()


class SingleSqueakUploadSync(UploadSync):

    def __init__(
        self,
        squeak_controller,
        timeout_s,
        squeak_hash: bytes,
    ):
        super().__init__(
            squeak_controller,
            timeout_s,
        )
        self.squeak_hash = squeak_hash

    def sync_peer(self, peer_connection):
        peer_connection.upload_single_squeak(self.squeak_hash)
