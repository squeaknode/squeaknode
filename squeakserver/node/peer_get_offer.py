import logging
import threading

from squeak.core.encryption import generate_data_key

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
    ):
        self.peer = peer
        self.squeak_hash = squeak_hash
        self.squeak_store = squeak_store
        self.postgres_db = postgres_db

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
        if (proof != challenge_proof):
            raise Exception("Invalid offer proof: {}, expected: {}".format(
                proof.hex(),
                challenge_proof.hex(),
            ))

        # Save the offer
        self._save_offer(offer)

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
        return self.peer_client.buy_squeak(self.squeak_hash, challenge)

    def _save_offer(self, offer):
        logger.info("Saving offer: {}".format(offer))
