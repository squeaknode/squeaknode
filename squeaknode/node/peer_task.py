import logging
import threading

from squeaknode.network.peer_client import PeerClient
from squeaknode.node.peer_get_offer import PeerGetOffer

logger = logging.getLogger(__name__)


LOOKUP_BLOCK_INTERVAL = 1008  # 1 week


class PeerSyncTask:
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

    def _get_local_squeak(self, squeak_hash):
        squeak_entry = self.squeak_store.get_squeak(squeak_hash)
        return squeak_entry.squeak

    def _upload_squeak(self, squeak_hash):
        logger.info("Uploading squeak: {}".format(squeak_hash.hex()))
        squeak = self._get_local_squeak(squeak_hash)
        self.peer_client.post_squeak(squeak)

    def _get_sharing_addresses(self):
        sharing_profiles = self.postgres_db.get_sharing_profiles()
        return [profile.address for profile in sharing_profiles]
