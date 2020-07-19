from squeak.core.encryption import (
    CEncryptedDecryptionKey,
    generate_initialization_vector,
)
from squeak.core.signing import CSigningKey, CSqueakAddress

from squeakserver.node.squeak_block_periodic_worker import SqueakBlockPeriodicWorker
from squeakserver.node.squeak_block_queue_worker import SqueakBlockQueueWorker
from squeakserver.node.squeak_block_verifier import SqueakBlockVerifier
from squeakserver.node.squeak_maker import SqueakMaker
from squeakserver.server.buy_offer import BuyOffer
from squeakserver.server.squeak_profile import SqueakProfile
from squeakserver.server.util import generate_offer_preimage


class SqueakNode:
    def __init__(
        self,
        postgres_db,
        blockchain_client,
        lightning_client,
        lightning_host_port,
        price,
    ):
        self.postgres_db = postgres_db
        self.blockchain_client = blockchain_client
        self.lightning_client = lightning_client
        self.lightning_host_port = lightning_host_port
        self.price = price
        self.squeak_block_verifier = SqueakBlockVerifier(postgres_db, blockchain_client)
        self.squeak_block_periodic_worker = SqueakBlockPeriodicWorker(
            self.squeak_block_verifier
        )
        self.squeak_block_queue_worker = SqueakBlockQueueWorker(
            self.squeak_block_verifier
        )

    def start_running(self):
        # self.squeak_block_periodic_worker.start_running()
        self.squeak_block_queue_worker.start_running()

    def save_squeak(self, squeak):
        inserted_squeak_hash = self.postgres_db.insert_squeak(squeak)
        self.squeak_block_verifier.add_squeak_to_queue(inserted_squeak_hash)
        return inserted_squeak_hash

    def get_locked_squeak(self, squeak_hash):
        squeak_entry = self.postgres_db.get_squeak_entry(squeak_hash)
        squeak = squeak_entry.squeak
        # Remove the decryption key before returning.
        squeak.ClearDecryptionKey()
        return squeak

    def get_squeak_entry(self, squeak_hash):
        return self.postgres_db.get_squeak_entry(squeak_hash)

    def lookup_squeaks(self, addresses, min_block, max_block):
        return self.postgres_db.lookup_squeaks(addresses, min_block, max_block)

    def get_buy_offer(self, squeak_hash, challenge):
        # Get the squeak from the database
        squeak_entry = self.postgres_db.get_squeak_entry(squeak_hash)
        squeak = squeak_entry.squeak
        # Get the decryption key from the squeak
        decryption_key = squeak.GetDecryptionKey()
        # Solve the proof
        proof = decryption_key.decrypt(challenge)
        # Generate a new random preimage
        preimage = generate_offer_preimage()
        # Encrypt the decryption key
        iv = generate_initialization_vector()
        encrypted_decryption_key = CEncryptedDecryptionKey.from_decryption_key(
            decryption_key, preimage, iv
        )
        # Get the offer price
        amount = self.price
        # Create the lightning invoice
        add_invoice_response = self.lightning_client.add_invoice(preimage, amount)
        preimage_hash = add_invoice_response.r_hash
        invoice_payment_request = add_invoice_response.payment_request
        # Get the lightning network node pubkey
        get_info_response = self.lightning_client.get_info()
        pubkey = get_info_response.identity_pubkey
        # Return the buy offer
        return BuyOffer(
            squeak_hash,
            encrypted_decryption_key,
            iv,
            amount,
            preimage_hash,
            invoice_payment_request,
            pubkey,
            self.lightning_host_port.host,
            self.lightning_host_port.port,
            proof,
        )

    def create_signing_profile(self, profile_name):
        signing_key = CSigningKey.generate()
        verifying_key = signing_key.get_verifying_key()
        address = CSqueakAddress.from_verifying_key(verifying_key)
        signing_key_str = str(signing_key)
        signing_key_bytes = signing_key_str.encode()
        squeak_profile = SqueakProfile(
            profile_id=None,
            profile_name=profile_name,
            private_key=signing_key_bytes,
            address=str(address),
            sharing=False,
            following=False,
        )
        return self.postgres_db.insert_profile(squeak_profile)

    def get_squeak_profile(self, profile_id):
        return self.postgres_db.get_profile(profile_id)

    def make_squeak(self, profile_id, content_str, replyto_hash):
        squeak_profile = self.postgres_db.get_profile(profile_id)
        squeak_maker = SqueakMaker(self.lightning_client)
        squeak = squeak_maker.make_squeak(squeak_profile, content_str, replyto_hash)
        return self.save_squeak(squeak)
