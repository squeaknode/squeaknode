import logging
import threading

from squeakserver.server.util import get_hash
from squeakserver.network.peer_client import PeerClient

logger = logging.getLogger(__name__)


LOOKUP_BLOCK_INTERVAL = 1008  # 1 week


class PeerDownloadTask:
    def __init__(
            self,
            peer,
            block_height,
            squeak_store,
            postgres_db,
            squeak_sync_status,
            lookup_block_interval=LOOKUP_BLOCK_INTERVAL,
    ):
        self.peer = peer
        self.block_height = block_height
        self.squeak_store = squeak_store
        self.postgres_db = postgres_db
        self.squeak_sync_status = squeak_sync_status
        self.lookup_block_interval = lookup_block_interval
        self._stop_event = threading.Event()

    class DownloadingContextManager():
        def __init__(self, peer, stopped, squeak_sync_status):
            logger.info('init method called')
            self.peer = peer
            self.stopped = stopped
            self.squeak_sync_status = squeak_sync_status

            if self.squeak_sync_status.is_downloading(self.peer):
                raise Exception("Peer is already downloading: {}".format(self.peer))

        def __enter__(self):
            logger.info('enter method called')
            self.squeak_sync_status.add_download(self.peer, self.stopped)
            logger.info('current downloads: {}'.format(self.squeak_sync_status.get_current_downloads()))
            return self

        def __exit__(self, exc_type, exc_value, exc_traceback):
            logger.info('exit method called')
            self.squeak_sync_status.remove_download(self.peer)

    def download(self):
        try:
            with self.DownloadingContextManager(self.peer, None, self.squeak_sync_status) as downloading_manager:
                self.download_from_peer()
        except Exception as e:
            logger.error("Download from peer failed.", exc_info=True)

    def download_from_peer(self):
        # Get list of followed addresses.
        addresses = self._get_followed_addresses()
        logger.info("Followed addresses: {}".format(addresses))
        min_block = self.block_height - self.lookup_block_interval
        max_block = self.block_height

        # Get remote hashes
        remote_hashes = self._get_remote_hashes(addresses, min_block, max_block)
        logger.info("Got remote hashes: {}".format(remote_hashes))

        # Get local hashes
        local_hashes = self._get_local_hashes(addresses, min_block, max_block)
        logger.info("Got local hashes: {}".format(local_hashes))

        # Get hashes to download
        hashes_to_download = set(remote_hashes) - set(local_hashes)
        logger.info("Hashes to download: {}".format(hashes_to_download))

    def stop(self):
        self._stop_event.set()

    def stopped(self):
        return self._stop_event.is_set()

    def _get_local_hashes(self, addresses, min_block, max_block):
        return self.squeak_store.lookup_squeaks(addresses, min_block, max_block)

    def _get_remote_hashes(self, addresses, min_block, max_block):
        peer_client = PeerClient(
            self.peer.host,
            self.peer.port,
        )
        return peer_client.lookup_squeaks(addresses, min_block, max_block)

    def _get_followed_addresses(self):
        followed_profiles = self.postgres_db.get_following_profiles()
        return [
            profile.address
            for profile in followed_profiles
        ]
