import logging

from squeaknode.core.util import get_hash

logger = logging.getLogger(__name__)


class PeerSyncTask:
    def __init__(
        self,
        peer_connection,
        squeak_controller,
    ):
        self.peer_connection = peer_connection
        self.squeak_controller = squeak_controller

    @property
    def peer(self):
        return self.peer_connection.peer

    @property
    def squeak_store(self):
        return self.squeak_controller.squeak_store

    @property
    def squeak_db(self):
        return self.squeak_controller.squeak_db

    @property
    def peer_client(self):
        return self.peer_connection.peer_client

    def download(
        self,
        min_block,
        max_block,
    ):
        # Get list of followed addresses.
        addresses = self._get_followed_addresses()
        logger.debug("Followed addresses: {}".format(addresses))

        # Get remote hashes
        lookup_result = self._get_remote_hashes(
            addresses, min_block, max_block)
        remote_hashes = lookup_result.hashes
        logger.debug("Got remote hashes: {}".format(len(remote_hashes)))
        for hash in remote_hashes:
            logger.debug("remote hash: {}".format(hash))

        # Get local hashes of downloaded squeaks
        local_hashes = self._get_local_hashes(addresses, min_block, max_block)
        logger.debug("Got local hashes: {}".format(len(local_hashes)))
        for hash in local_hashes:
            logger.debug("local hash: {}".format(hash))

        # Get hashes to download
        hashes_to_download = set(remote_hashes) - set(local_hashes)
        logger.debug("Hashes to download: {}".format(len(hashes_to_download)))
        for hash in hashes_to_download:
            logger.debug("hash to download: {}".format(hash))

        # Download squeaks for the hashes
        # TODO: catch exception downloading individual squeak
        for hash in hashes_to_download:
            if self.peer_connection.stopped():
                return
            self._download_squeak(bytes.fromhex(hash))

        # Get local hashes of locked squeaks that don't have an offer from this peer.
        locked_hashes = self._get_locked_hashes(
            addresses, min_block, max_block)
        logger.debug("Got locked hashes: {}".format(len(locked_hashes)))
        for hash in locked_hashes:
            logger.debug("locked hash: {}".format(hash))

        # Get hashes to get offer
        hashes_to_get_offer = set(remote_hashes) & set(locked_hashes)
        logger.debug("Hashes to get offer: {}".format(
            len(hashes_to_get_offer)))
        for hash in hashes_to_get_offer:
            logger.debug("hash to get offer: {}".format(hash))

        # Download offers for the hashes
        # TODO: catch exception downloading individual squeak
        for hash in hashes_to_get_offer:
            if self.peer_connection.stopped():
                return
            self._download_offer(bytes.fromhex(hash))

    def upload(
        self,
        min_block,
        max_block,
    ):
        # Get list of sharing addresses.
        addresses = self._get_sharing_addresses()
        logger.debug("Sharing addresses: {}".format(addresses))

        # Get remote hashes
        lookup_result = self._get_remote_hashes(
            addresses, min_block, max_block)
        remote_hashes = lookup_result.hashes
        allowed_addresses = lookup_result.allowed_addresses
        logger.debug("Got remote hashes: {}".format(len(remote_hashes)))
        for hash in remote_hashes:
            logger.debug("remote hash: {}".format(hash))

        # Get local hashes
        local_hashes = self._get_local_unlocked_hashes(
            addresses, min_block, max_block)
        logger.debug("Got local hashes: {}".format(len(local_hashes)))
        for hash in local_hashes:
            logger.debug("local hash: {}".format(hash))

        # Get hashes to upload
        hashes_to_upload = set(local_hashes) - set(remote_hashes)
        logger.debug("Hashes to upload: {}".format(len(hashes_to_upload)))
        for hash in hashes_to_upload:
            logger.debug("hash to upload: {}".format(hash))

        # Upload squeaks for the hashes
        # TODO: catch exception uploading individual squeak
        for hash in hashes_to_upload:
            if self.peer_connection.stopped():
                return
            self._try_upload_squeak(
                bytes.fromhex(hash),
                allowed_addresses,
            )

    def download_single_squeak(self, squeak_hash: bytes):
        logger.info("download_single_squeak with hash: {}".format(
            squeak_hash.hex()))

        # Download squeak if not already present.
        saved_squeak = self._get_local_squeak(squeak_hash)
        logger.info(
            "download_single_squeak with saved_squeak: {}".format(saved_squeak))
        if not saved_squeak:
            self._download_squeak(squeak_hash)

        # Download offer from peer if not already present.
        saved_offer = self._get_saved_offer(squeak_hash)
        logger.info(
            "download_single_squeak with saved_offer: {}".format(saved_offer))
        if not saved_offer:
            self._download_offer(squeak_hash)

    def upload_single_squeak(self, squeak_hash: bytes):
        # Download squeak if not already present.
        local_squeak = self._get_local_squeak(squeak_hash)
        if local_squeak and local_squeak.HasDecryptionKey():
            self._upload_squeak(local_squeak)

    def get_offer(self, squeak_hash: bytes):
        logger.info("Getting offer for squeak hash: {}".format(
            squeak_hash.hex()))

        # Get the squeak from the squeak hash
        squeak = self._get_local_squeak(squeak_hash)

        # Download the buy offer
        offer_msg = self._download_offer_msg(squeak_hash)

        decoded_offer = self.squeak_controller.get_offer(
            squeak, offer_msg, self.peer)

        # Save the offer
        self._save_offer(decoded_offer)

    def _get_local_hashes(self, addresses, min_block, max_block):
        return self.squeak_store.lookup_squeaks_include_locked(
            addresses,
            min_block,
            max_block,
        )

    def _get_local_unlocked_hashes(self, addresses, min_block, max_block):
        return self.squeak_store.lookup_squeaks(addresses, min_block, max_block)

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
        # self.squeak_store.save_squeak(squeak, skip_whitelist_check=True)
        self.squeak_controller.save_downloaded_squeak(squeak)

    def _get_saved_offer(self, squeak_hash: bytes):
        logger.info("Getting saved offer for hash: {}".format(
            squeak_hash.hex()))
        offers = self.squeak_db.get_offers_with_peer(squeak_hash)
        for offer_with_peer in offers:
            if offer_with_peer.offer.peer_id == self.peer.peer_id:
                return offer_with_peer

    def _download_squeak(self, squeak_hash: bytes):
        logger.info(
            "Downloading squeak: {} from peer: {}".format(
                squeak_hash.hex(), self.peer.peer_id
            )
        )
        squeak = self.peer_client.get_squeak(squeak_hash)
        self._save_squeak(squeak)

    def _get_followed_addresses(self):
        followed_profiles = self.squeak_db.get_following_profiles()
        return [profile.address for profile in followed_profiles]

    def _download_offer(self, squeak_hash: bytes):
        logger.info("Downloading offer for hash: {}".format(squeak_hash.hex()))
        self.get_offer(squeak_hash)

    def _get_local_squeak(self, squeak_hash: bytes):
        return self.squeak_store.get_squeak(squeak_hash)

    def _try_upload_squeak(self, squeak_hash: bytes, allowed_addresses):
        squeak = self._get_local_squeak(squeak_hash)
        squeak_address = str(squeak.GetAddress())
        if squeak_address in allowed_addresses:
            self._upload_squeak(squeak)

    def _upload_squeak(self, squeak):
        logger.info("Uploading squeak: {}".format(
            get_hash(squeak).hex()
        ))
        self.peer_client.post_squeak(squeak)

    def _get_sharing_addresses(self):
        sharing_profiles = self.squeak_db.get_sharing_profiles()
        return [profile.address for profile in sharing_profiles]

    def _download_offer_msg(self, squeak_hash: bytes):
        logger.info(
            "Downloading buy offer for squeak hash: {}".format(squeak_hash.hex()))
        return self.peer_client.buy_squeak(squeak_hash)

    def _save_offer(self, offer):
        logger.info("Saving offer: {}".format(offer))
        self.squeak_db.insert_offer(offer)
