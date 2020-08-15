import logging
import threading

from squeakserver.server.util import get_hash
from squeakserver.network.peer_client import PeerClient
from squeakserver.node.peer_get_offer import PeerGetOffer

logger = logging.getLogger(__name__)


LOOKUP_BLOCK_INTERVAL = 1008  # 1 week


class PeerDownload:
    def __init__(
            self,
            peer,
            block_height,
            squeak_store,
            postgres_db,
            lightning_client,
            lookup_block_interval=LOOKUP_BLOCK_INTERVAL,
    ):
        self.peer = peer
        self.block_height = block_height
        self.squeak_store = squeak_store
        self.postgres_db = postgres_db
        self.lightning_client = lightning_client
        self.lookup_block_interval = lookup_block_interval

        self.peer_client = PeerClient(
            self.peer.host,
            self.peer.port,
        )

        self._stop_event = threading.Event()

    def download(self):
        # Get list of followed addresses.
        addresses = self._get_followed_addresses()
        logger.info("Followed addresses: {}".format(addresses))
        min_block = self.block_height - self.lookup_block_interval
        max_block = self.block_height

        if self.stopped():
            return

        # Get remote hashes
        remote_hashes = self._get_remote_hashes(addresses, min_block, max_block)
        logger.info("Got remote hashes: {}".format(len(remote_hashes)))
        for hash in remote_hashes:
            logger.info("remote hash: {}".format(hash.hex()))

        if self.stopped():
            return

        # Get local hashes of downloaded squeaks
        local_hashes = self._get_local_hashes(addresses, min_block, max_block)
        logger.info("Got local hashes: {}".format(len(local_hashes)))
        for hash in local_hashes:
            logger.info("local hash: {}".format(hash.hex()))

        if self.stopped():
            return

        # Get local hashes of locked squeaks that don't have an offer from this peer.
        locked_hashes = self._get_locked_hashes(addresses, min_block, max_block)
        logger.info("Got locked hashes: {}".format(len(locked_hashes)))
        for hash in locked_hashes:
            logger.info("locked hash: {}".format(hash.hex()))

        if self.stopped():
            return

        # Get hashes to download
        hashes_to_download = set(remote_hashes) - set(local_hashes)
        logger.info("Hashes to download: {}".format(len(hashes_to_download)))
        for hash in hashes_to_download:
            logger.info("hash to download: {}".format(hash.hex()))

        # Get hashes to get offer
        hashes_to_get_offer = set(remote_hashes) & set(locked_hashes)
        logger.info("Hashes to get offer: {}".format(len(hashes_to_get_offer)))
        for hash in hashes_to_get_offer:
            logger.info("hash to get offer: {}".format(hash.hex()))

        # Download squeaks for the hashes
        # TODO: catch exception downloading individual squeak
        for hash in hashes_to_download:
            if self.stopped():
                return
            self._download_squeak(hash)

        # Download offers for the hashes
        # TODO: catch exception downloading individual squeak
        for hash in hashes_to_get_offer:
            if self.stopped():
                return
            self._download_offer(hash)

    def stop(self):
        self._stop_event.set()

    def stopped(self):
        return self._stop_event.is_set()

    def _get_local_hashes(self, addresses, min_block, max_block):
        return self.squeak_store.lookup_squeaks_include_locked(
            addresses,
            min_block,
            max_block,
        )

    def _get_locked_hashes(self, addresses, min_block, max_block):
        return self.squeak_store.lookup_squeaks_needing_offer(
            addresses,
            min_block,
            max_block,
            self.peer.peer_id,
        )

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

    def _download_offer(self, squeak_hash):
        logger.info("Downloading offer for hash: {}".format(squeak_hash.hex()))
        peer_get_offer = PeerGetOffer(
            self.peer,
            squeak_hash,
            self.squeak_store,
            self.postgres_db,
            self.lightning_client,
        )
        peer_get_offer.get_offer()
