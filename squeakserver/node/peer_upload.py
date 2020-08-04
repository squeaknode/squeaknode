import logging
import threading

from squeakserver.server.util import get_hash
from squeakserver.network.peer_client import PeerClient

logger = logging.getLogger(__name__)


LOOKUP_BLOCK_INTERVAL = 1008  # 1 week


class PeerUpload:
    def __init__(
            self,
            peer,
            block_height,
            squeak_store,
            postgres_db,
            lookup_block_interval=LOOKUP_BLOCK_INTERVAL,
    ):
        self.peer = peer
        self.block_height = block_height
        self.squeak_store = squeak_store
        self.postgres_db = postgres_db
        self.lookup_block_interval = lookup_block_interval
        self._stop_event = threading.Event()

    def upload(self):
        # Get list of sharing addresses.
        addresses = self._get_sharing_addresses()
        logger.info("Sharing addresses: {}".format(addresses))
        min_block = self.block_height - self.lookup_block_interval
        max_block = self.block_height

        if self.stopped():
            return

        # Get remote hashes
        remote_hashes = self._get_remote_hashes(addresses, min_block, max_block)
        logger.info("Got remote hashes: {}".format(remote_hashes))

        if self.stopped():
            return

        # Get local hashes
        local_hashes = self._get_local_hashes(addresses, min_block, max_block)
        logger.info("Got local hashes: {}".format(local_hashes))

        if self.stopped():
            return

        # Get hashes to upload
        hashes_to_upload = set(local_hashes) - set(remote_hashes)
        logger.info("Hashes to upload: {}".format(hashes_to_upload))

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

    def _get_sharing_addresses(self):
        sharing_profiles = self.postgres_db.get_sharing_profiles()
        return [
            profile.address
            for profile in sharing_profiles
        ]
