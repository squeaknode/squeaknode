import logging
import threading

from squeak.core.encryption import generate_data_key

from squeakserver.core.offer import Offer
from squeakserver.server.util import get_hash
from squeakserver.network.peer_client import PeerClient

logger = logging.getLogger(__name__)


class PeerGetOffer:
    def __init__(
            self,
            peer,
            squeak_hash,
            squeak_store,
            postgres_db,
            lightning_client
    ):
        self.peer = peer
        self.squeak_hash = squeak_hash
        self.squeak_store = squeak_store
        self.postgres_db = postgres_db
        self.lightning_client = lightning_client

        self.peer_client = PeerClient(
            self.peer.host,
            self.peer.port,
        )

        self._stop_event = threading.Event()

    def get_offer(self):
        logger.info("Getting offer for squeak hash: {}".format(self.squeak_hash.hex()))

        # TODO: check if there is already an offer from this peer, and delete it

        # Get the squeak from the squeak hash
        squeak = self._get_squeak()

        # Get the encryption key
        encryption_key = squeak.GetEncryptionKey()

        # Create a new challenge
        challenge_proof = self._generate_challenge_proof()
        challenge = self._get_challenge(challenge_proof, encryption_key)

        # Download the buy offer
        offer = self._download_buy_offer(challenge)

        # Check the proof
        proof = offer.proof
        logger.info("Proof: {}".format(proof.hex()))
        logger.info("Expected proof: {}".format(challenge_proof.hex()))
        if (proof != challenge_proof):
            raise Exception("Invalid offer proof: {}, expected: {}".format(
                proof.hex(),
                challenge_proof.hex(),
            ))

        # Get the decoded offer from the payment request string
        decoded_offer = self._get_decoded_offer(offer)

        # Save the offer
        self._save_offer(decoded_offer)

    def stop(self):
        self._stop_event.set()

    def stopped(self):
        return self._stop_event.is_set()

    def _get_squeak(self):
        squeak_entry = self.squeak_store.get_squeak(self.squeak_hash)
        return squeak_entry.squeak

    def _generate_challenge_proof(self):
        return generate_data_key()

    def _get_challenge(self, challenge_proof, encryption_key):
        return encryption_key.encrypt(challenge_proof)

    def _download_buy_offer(self, challenge):
        logger.info("Downloading buy offer for squeak hash: {}".format(self.squeak_hash.hex()))
        offer_msg = self.peer_client.buy_squeak(self.squeak_hash, challenge)
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
            amount=offer_msg.amount,
            preimage_hash=offer_msg.preimage_hash,
            payment_request=offer_msg.payment_request,
            node_pubkey=offer_msg.pubkey,
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
        # TODO create a new offer object with decoded fields
        return offer
