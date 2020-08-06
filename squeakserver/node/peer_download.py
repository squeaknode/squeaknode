import logging
import threading

from squeakserver.server.util import get_hash
from squeakserver.network.peer_client import PeerClient

logger = logging.getLogger(__name__)


LOOKUP_BLOCK_INTERVAL = 1008  # 1 week


class PeerDownload:
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

    def download(self):
        # Get list of followed addresses.
        addresses = self._get_followed_addresses()
        logger.debug("Followed addresses: {}".format(addresses))
        min_block = self.block_height - self.lookup_block_interval
        max_block = self.block_height

        if self.stopped():
            return

        # Get remote hashes
        remote_hashes = self._get_remote_hashes(addresses, min_block, max_block)
        # logger.info("Got remote hashes: {}".format(remote_hashes))
        # logger.info("Got remote hashes: {}".format([hash.hex() for hash in remote_hashes]))
        logger.info("Got remote hashes: {}".format(len(remote_hashes)))
        for hash in remote_hashes:
            logger.info("remote hash: {}".format(hash.hex()))

        if self.stopped():
            return

        # Get local hashes
        local_hashes = self._get_local_hashes(addresses, min_block, max_block)
        # logger.info("Got local hashes: {}".format(local_hashes))
        # logger.info("Got local hashes: {}".format([hash.hex() for hash in local_hashes]))
        logger.info("Got local hashes: {}".format(len(local_hashes)))
        for hash in local_hashes:
            logger.info("local hash: {}".format(hash.hex()))

        if self.stopped():
            return

        # Get hashes to download
        hashes_to_download = set(remote_hashes) - set(local_hashes)
        # logger.info("Hashes to download: {}".format(hashes_to_download))
        # logger.info("Hashes to download: {}".format([hash.hex() for hash in hashes_to_download]))
        logger.info("Hashes to download: {}".format(len(hashes_to_download)))
        for hash in hashes_to_download:
            logger.info("hash to download: {}".format(hash.hex()))

        # Download squeaks for the hashes
        for hash in hashes_to_download:
            if self.stopped():
                return
            self._download_squeak(hash)

    def stop(self):
        self._stop_event.set()

    def stopped(self):
        return self._stop_event.is_set()

    def _get_local_hashes(self, addresses, min_block, max_block):
        return self.squeak_store.lookup_squeaks(addresses, min_block, max_block)

    def _get_remote_hashes(self, addresses, min_block, max_block):
        return self.peer_client.lookup_squeaks(addresses, min_block, max_block)

    def _save_squeak(self, squeak):
        self.squeak_store.save_downloaded_squeak(squeak)

    def _download_squeak(self, squeak_hash):
        logger.info("Downloading squeak: {}".format(squeak_hash.hex()))
        squeak = self.peer_client.get_squeak(squeak_hash)
        self._save_squeak(squeak)

    def _get_followed_addresses(self):
        followed_profiles = self.postgres_db.get_following_profiles()
        return [
            profile.address
            for profile in followed_profiles
        ]
