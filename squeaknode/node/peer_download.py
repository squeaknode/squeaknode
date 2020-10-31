import logging
import threading

from squeaknode.network.peer_client import PeerClient
from squeaknode.node.peer_get_offer import PeerGetOffer

logger = logging.getLogger(__name__)


LOOKUP_BLOCK_INTERVAL = 1008  # 1 week


class PeerDownload:
    def __init__(
        self,
        peer,
        squeak_store,
        postgres_db,
        lightning_client,
    ):
        self.peer = peer
        self.squeak_store = squeak_store
        self.postgres_db = postgres_db
        self.lightning_client = lightning_client

        self.peer_client = PeerClient(
            self.peer.host,
            self.peer.port,
        )

        self._stop_event = threading.Event()

    def download(
        self,
        block_height,
        lookup_block_interval=LOOKUP_BLOCK_INTERVAL,
    ):
        # Get list of followed addresses.
        addresses = self._get_followed_addresses()
        logger.debug("Followed addresses: {}".format(addresses))
        min_block = block_height - lookup_block_interval
        max_block = block_height

        # Get remote hashes
        remote_hashes = self._get_remote_hashes(addresses, min_block, max_block)
        logger.debug("Got remote hashes: {}".format(len(remote_hashes)))
        for hash in remote_hashes:
            logger.debug("remote hash: {}".format(hash.hex()))

        # Get local hashes of downloaded squeaks
        local_hashes = self._get_local_hashes(addresses, min_block, max_block)
        logger.debug("Got local hashes: {}".format(len(local_hashes)))
        for hash in local_hashes:
            logger.debug("local hash: {}".format(hash.hex()))

        # Get hashes to download
        hashes_to_download = set(remote_hashes) - set(local_hashes)
        logger.debug("Hashes to download: {}".format(len(hashes_to_download)))
        for hash in hashes_to_download:
            logger.debug("hash to download: {}".format(hash.hex()))

        # Download squeaks for the hashes
        # TODO: catch exception downloading individual squeak
        for hash in hashes_to_download:
            if self.stopped():
                return
            self._download_squeak(hash)

        # Get local hashes of locked squeaks that don't have an offer from this peer.
        locked_hashes = self._get_locked_hashes(addresses, min_block, max_block)
        logger.debug("Got locked hashes: {}".format(len(locked_hashes)))
        for hash in locked_hashes:
            logger.debug("locked hash: {}".format(hash.hex()))

        # Get hashes to get offer
        hashes_to_get_offer = set(remote_hashes) & set(locked_hashes)
        logger.debug("Hashes to get offer: {}".format(len(hashes_to_get_offer)))
        for hash in hashes_to_get_offer:
            logger.debug("hash to get offer: {}".format(hash.hex()))

        # Download offers for the hashes
        # TODO: catch exception downloading individual squeak
        for hash in hashes_to_get_offer:
            if self.stopped():
                return
            self._download_offer(hash)

    def download_single_squeak(self, squeak_hash):
        # Download squeak if not already present.
        saved_squeak = self._get_saved_squeak(squeak_hash)
        if not saved_squeak:
            self._download_squeak(squeak_hash)

        # Download offer from peer if not already present.
        saved_offer = self._get_saved_offer(squeak_hash)
        if not saved_offer:
            self._download_offer(squeak_hash)

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

    def _get_saved_squeak(self, squeak_hash):
        return self.squeak_store.get_squeak(squeak_hash)
        return self.postgres_db.get_offers_with_peer(squeak_hash_str)

    def _get_saved_offer(self, squeak_hash):
        offers = self.postgres_db.get_offers_with_peer(squeak_hash)
        for offer in offers:
            if offer.peer_id == peer_id:
                return offer

    def _download_squeak(self, squeak_hash):
        logger.info("Downloading squeak: {} from peer: {}".format(squeak_hash.hex(), self.peer.peer_id))
        squeak = self.peer_client.get_squeak(squeak_hash)
        self._save_squeak(squeak)

    def _get_followed_addresses(self):
        followed_profiles = self.postgres_db.get_following_profiles()
        return [profile.address for profile in followed_profiles]

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
