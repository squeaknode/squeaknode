import logging
import threading


from squeak.core.encryption import generate_data_key

from squeaknode.core.offer import Offer
from squeaknode.network.peer_client import PeerClient
from squeaknode.server.util import get_hash, get_replyto

logger = logging.getLogger(__name__)


LOOKUP_BLOCK_INTERVAL = 1008  # 1 week


class PeerSyncTask:
    def __init__(
        self,
        peer_connection,
        squeak_store,
        postgres_db,
        lightning_client,
    ):
        self.peer_connection = peer_connection
        self.squeak_store = squeak_store
        self.postgres_db = postgres_db
        self.lightning_client = lightning_client

    @property
    def peer(self):
        return self.peer_connection.peer

    @property
    def peer_client(self):
        return self.peer_connection.peer_client

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
        lookup_result = self._get_remote_hashes(addresses, min_block, max_block)
        remote_hashes = lookup_result.hashes
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
            if self.peer_connection.stopped():
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
            if self.peer_connection.stopped():
                return
            self._download_offer(hash)

    def upload(
        self,
        block_height,
        lookup_block_interval=LOOKUP_BLOCK_INTERVAL,
    ):
        # Get list of sharing addresses.
        addresses = self._get_sharing_addresses()
        logger.debug("Sharing addresses: {}".format(addresses))
        min_block = block_height - lookup_block_interval
        max_block = block_height

        # Get remote hashes
        lookup_result = self._get_remote_hashes(addresses, min_block, max_block)
        remote_hashes = lookup_result.hashes
        allowed_addresses = lookup_result.allowed_addresses
        logger.debug("Got remote hashes: {}".format(len(remote_hashes)))
        for hash in remote_hashes:
            logger.debug("remote hash: {}".format(hash.hex()))

        # Get local hashes
        local_hashes = self._get_local_unlocked_hashes(addresses, min_block, max_block)
        logger.debug("Got local hashes: {}".format(len(local_hashes)))
        for hash in local_hashes:
            logger.debug("local hash: {}".format(hash.hex()))

        # Get hashes to upload
        hashes_to_upload = set(local_hashes) - set(remote_hashes)
        logger.debug("Hashes to upload: {}".format(len(hashes_to_upload)))
        for hash in hashes_to_upload:
            logger.debug("hash to upload: {}".format(hash.hex()))

        # Upload squeaks for the hashes
        # TODO: catch exception uploading individual squeak
        for hash in hashes_to_upload:
            if self.peer_connection.stopped():
                return
            self._try_upload_squeak(hash, allowed_addresses)

    def download_single_squeak(self, squeak_hash):
        # Download squeak if not already present.
        saved_squeak = self._get_local_squeak(squeak_hash)
        if not saved_squeak:
            self._download_squeak(squeak_hash)

        # Download offer from peer if not already present.
        saved_offer = self._get_saved_offer(squeak_hash)
        if not saved_offer:
            self._download_offer(squeak_hash)

    def upload_single_squeak(self, squeak_hash):
        # Download squeak if not already present.
        local_squeak = self._get_local_squeak(squeak_hash)
        if local_squeak and local_squeak.HasDecryptionKey():
            self._upload_squeak(local_squeak)

    def get_offer(self, squeak_hash):
        logger.info("Getting offer for squeak hash: {}".format(squeak_hash.hex()))

        # Get the squeak from the squeak hash
        squeak = self._get_local_squeak(squeak_hash)

        # Get the encryption key
        encryption_key = squeak.GetEncryptionKey()

        # Create a new challenge
        challenge_proof = self._generate_challenge_proof()
        challenge = self._get_challenge(challenge_proof, encryption_key)

        # Download the buy offer
        offer = self._download_buy_offer(squeak_hash, challenge)

        # Check the proof
        proof = offer.proof
        logger.info("Proof: {}".format(proof.hex()))
        logger.info("Expected proof: {}".format(challenge_proof.hex()))
        if proof != challenge_proof:
            raise Exception(
                "Invalid offer proof: {}, expected: {}".format(
                    proof.hex(),
                    challenge_proof.hex(),
                )
            )

        # Get the decoded offer from the payment request string
        decoded_offer = self._get_decoded_offer(offer)

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
        self.squeak_store.save_squeak(squeak, verify=True, skip_whitelist_check=True)

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
        self.get_offer(squeak_hash)

    def _get_local_squeak(self, squeak_hash):
        return self.squeak_store.get_squeak(squeak_hash)

    def _try_upload_squeak(self, squeak_hash, allowed_addresses):
        squeak = self._get_local_squeak(squeak_hash)
        squeak_address = str(squeak.GetAddress())
        if squeak_address in allowed_addresses:
            self._upload_squeak(squeak)

    def _upload_squeak(self, squeak):
        squeak_hash = get_hash(squeak)
        logger.info("Uploading squeak: {}".format(squeak_hash.hex()))
        self.peer_client.post_squeak(squeak)

    def _get_sharing_addresses(self):
        sharing_profiles = self.postgres_db.get_sharing_profiles()
        return [profile.address for profile in sharing_profiles]

    def _generate_challenge_proof(self):
        return generate_data_key()

    def _get_challenge(self, challenge_proof, encryption_key):
        return encryption_key.encrypt(challenge_proof)

    def _download_buy_offer(self, squeak_hash, challenge):
        logger.info(
            "Downloading buy offer for squeak hash: {}".format(squeak_hash.hex())
        )
        offer_msg = self.peer_client.buy_squeak(squeak_hash, challenge)
        offer = self._offer_from_msg(offer_msg)
        return offer

    def _save_offer(self, offer):
        logger.info("Saving offer: {}".format(offer))
        self.postgres_db.insert_offer(offer)

    def _offer_from_msg(self, offer_msg):
        if not offer_msg:
            return None
        return Offer(
            offer_id=None,
            squeak_hash=offer_msg.squeak_hash,
            key_cipher=offer_msg.key_cipher,
            iv=offer_msg.iv,
            price_msat=None,
            payment_hash=offer_msg.preimage_hash,
            invoice_timestamp=None,
            invoice_expiry=None,
            payment_request=offer_msg.payment_request,
            destination=None,
            node_host=offer_msg.host,
            node_port=offer_msg.port,
            proof=offer_msg.proof,
            peer_id=self.peer.peer_id,
        )

    def _decode_payment_request(self, payment_request):
        return self.lightning_client.decode_pay_req(payment_request)

    def _get_decoded_offer(self, offer):
        pay_req = self._decode_payment_request(offer.payment_request)
        logger.info("Decoded payment request: {}".format(pay_req))

        price_msat = pay_req.num_msat
        destination = pay_req.destination
        invoice_timestamp = pay_req.timestamp
        invoice_expiry = pay_req.expiry
        node_host = offer.node_host or self.peer.host
        node_port = offer.node_port

        logger.info("price_msat: {}".format(price_msat))
        logger.info("destination: {}".format(destination))
        logger.info("invoice_timestamp: {}".format(invoice_timestamp))
        logger.info("invoice_expiry: {}".format(invoice_expiry))
        logger.info("node_host: {}".format(node_host))
        logger.info("node_port: {}".format(node_port))

        decoded_offer = Offer(
            offer_id=offer.offer_id,
            squeak_hash=offer.squeak_hash,
            key_cipher=offer.key_cipher,
            iv=offer.iv,
            price_msat=price_msat,
            payment_hash=offer.payment_hash,
            invoice_timestamp=invoice_timestamp,
            invoice_expiry=invoice_expiry,
            payment_request=offer.payment_request,
            destination=destination,
            node_host=node_host,
            node_port=node_port,
            proof=offer.proof,
            peer_id=offer.peer_id,
        )

        return decoded_offer
