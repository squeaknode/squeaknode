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

        self.peer_client = PeerClient(
            self.peer.host,
            self.peer.port,
        )

        self._stop_event = threading.Event()

    def upload(self):
        # Get list of sharing addresses.
        addresses = self._get_sharing_addresses()
        logger.debug("Sharing addresses: {}".format(addresses))
        min_block = self.block_height - self.lookup_block_interval
        max_block = self.block_height

        if self.stopped():
            return

        # Get remote hashes
        remote_hashes = self._get_remote_hashes(addresses, min_block, max_block)
        logger.debug("Got remote hashes: {}".format(len(remote_hashes)))
        for hash in remote_hashes:
            logger.debug("remote hash: {}".format(hash.hex()))

        if self.stopped():
            return

        # Get local hashes
        local_hashes = self._get_local_hashes(addresses, min_block, max_block)
        logger.debug("Got local hashes: {}".format(len(local_hashes)))
        for hash in local_hashes:
            logger.debug("local hash: {}".format(hash.hex()))

        if self.stopped():
            return

        # Get hashes to upload
        hashes_to_upload = set(local_hashes) - set(remote_hashes)
        logger.debug("Hashes to upload: {}".format(len(hashes_to_upload)))
        for hash in hashes_to_upload:
            logger.debug("hash to upload: {}".format(hash.hex()))

        # Upload squeaks for the hashes
        # TODO: catch exception uploading individual squeak
        for hash in hashes_to_upload:
            if self.stopped():
                return
            self._upload_squeak(hash)

    def stop(self):
        self._stop_event.set()

    def stopped(self):
        return self._stop_event.is_set()

    def _get_local_hashes(self, addresses, min_block, max_block):
        return self.squeak_store.lookup_squeaks(addresses, min_block, max_block)

    def _get_remote_hashes(self, addresses, min_block, max_block):
        return self.peer_client.lookup_squeaks(addresses, min_block, max_block)

    def _get_local_squeak(self, squeak_hash):
        squeak_entry = self.squeak_store.get_squeak(squeak_hash)
        return squeak_entry.squeak

    def _upload_squeak(self, squeak_hash):
        logger.info("Uploading squeak: {}".format(squeak_hash.hex()))
        squeak = self._get_local_squeak(squeak_hash)
        self.peer_client.post_squeak(squeak)

    def _get_sharing_addresses(self):
        sharing_profiles = self.postgres_db.get_sharing_profiles()
        return [
            profile.address
            for profile in sharing_profiles
        ]
