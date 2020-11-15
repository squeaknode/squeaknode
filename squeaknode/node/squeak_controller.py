import logging
from hashlib import sha256

from squeak.core.encryption import (
    CEncryptedDecryptionKey,
    generate_initialization_vector,
)
from squeak.core.signing import CSigningKey, CSqueakAddress
from squeak.core import CheckSqueak

from squeaknode.core.squeak_address_validator import SqueakAddressValidator
from squeaknode.node.squeak_block_verifier import SqueakBlockVerifier
from squeaknode.node.squeak_maker import SqueakMaker
from squeaknode.node.squeak_rate_limiter import SqueakRateLimiter
from squeaknode.node.squeak_store import SqueakStore
from squeaknode.node.squeak_sync_status import SqueakSyncController
from squeaknode.node.squeak_whitelist import SqueakWhitelist
from squeaknode.server.buy_offer import BuyOffer
from squeaknode.server.sent_offer import SentOffer
from squeaknode.server.squeak_peer import SqueakPeer
from squeaknode.server.squeak_profile import SqueakProfile
from squeaknode.server.sent_payment import SentPayment
from squeaknode.server.util import generate_offer_preimage
from squeaknode.node.sent_offers_verifier import SentOffersVerifier
from squeaknode.node.sent_offers_worker import SentOffersWorker


logger = logging.getLogger(__name__)


class SqueakController:
    def __init__(
        self,
        squeak_db,
        blockchain_client,
        lightning_client,
        lightning_host_port,
        price_msat,
        max_squeaks_per_address_per_hour,
    ):
        self.squeak_db = squeak_db
        self.blockchain_client = blockchain_client
        self.lightning_client = lightning_client
        self.lightning_host_port = lightning_host_port
        self.price_msat = price_msat
        self.squeak_block_verifier = SqueakBlockVerifier(squeak_db, blockchain_client)
        self.squeak_rate_limiter = SqueakRateLimiter(
            squeak_db,
            blockchain_client,
            lightning_client,
            max_squeaks_per_address_per_hour,
        )
        self.squeak_whitelist = SqueakWhitelist(
            squeak_db,
        )
        self.squeak_store = SqueakStore(
            squeak_db,
            self.squeak_block_verifier,
            self.squeak_rate_limiter,
            self.squeak_whitelist,
        )
        self.squeak_sync_controller = SqueakSyncController(
            self.blockchain_client,
            self.squeak_store,
            self.squeak_db,
            self.lightning_client,
        )
        self.sent_offers_verifier = SentOffersVerifier(
            self.squeak_db,
            self.lightning_client,
        )

    # def start_running(self):
    #     self.squeak_block_periodic_worker.start_running()
    #     self.squeak_block_queue_worker.start_running()
    #     self.squeak_peer_sync_worker.start_running()
    #     self.squeak_offer_expiry_worker.start_running()
    #     self.sent_offers_worker.start_running()

    def save_uploaded_squeak(self, squeak):
        return self.squeak_store.save_squeak(squeak)

    def save_created_squeak(self, squeak):
        return self.squeak_store.save_squeak(squeak, verify=True, skip_whitelist_check=True)

    def get_public_squeak(self, squeak_hash):
        return self.squeak_store.get_squeak(squeak_hash, clear_decryption_key=True)

    # def get_squeak_entry(self, squeak_hash):
    #     return self.squeak_store.get_squeak(squeak_hash)

    def lookup_squeaks(self, addresses, min_block, max_block):
        return self.squeak_store.lookup_squeaks(addresses, min_block, max_block)

    def lookup_allowed_addresses(self, addresses):
        return self.squeak_whitelist.get_allowed_addresses(addresses)

    def get_buy_offer(self, squeak_hash, challenge, client_addr):
        # Check if there is an existing offer for the hash/client_addr combination
        sent_offer = self.squeak_db.get_sent_offer_by_squeak_hash_and_client_addr(squeak_hash, client_addr)
        if sent_offer:
            return None
        sent_offer = self.create_offer(squeak_hash, challenge, client_addr)
        # Save the incoming potential payment in the databse.
        self.squeak_db.insert_sent_offer(sent_offer)
        # Get the squeak from the database
        squeak = self.squeak_store.get_squeak(squeak_hash)
        # Get the decryption key from the squeak
        decryption_key = squeak.GetDecryptionKey()
        # Solve the proof
        proof = decryption_key.decrypt(challenge)
        # Encrypt the decryption key
        iv = generate_initialization_vector()
        encrypted_decryption_key = CEncryptedDecryptionKey.from_decryption_key(
            decryption_key,
            bytes.fromhex(sent_offer.preimage),
            iv,
        )
        # Get the lightning network node pubkey
        get_info_response = self.lightning_client.get_info()
        pubkey = get_info_response.identity_pubkey
        # Get the invoice details
        #lookup_invoice_response = self.lightning_client.lookup_invoice(sent_offer.preimage_hash)
        #invoice_payment_request = lookup_invoice_response.payment_request
        # Return the buy offer
        return BuyOffer(
            squeak_hash,
            encrypted_decryption_key,
            iv,
            self.price_msat,
            bytes.fromhex(sent_offer.preimage_hash),
            sent_offer.payment_request,
            pubkey,
            self.lightning_host_port.host,
            self.lightning_host_port.port,
            proof,
        )

    def create_offer(self, squeak_hash, challenge, client_addr):
        # Generate a new random preimage
        preimage = generate_offer_preimage()
        # Create the lightning invoice
        add_invoice_response = self.lightning_client.add_invoice(preimage, self.price_msat)
        logger.info("add_invoice_response: {}".format(add_invoice_response))
        preimage_hash = add_invoice_response.r_hash
        invoice_payment_request = add_invoice_response.payment_request
        # invoice_expiry = add_invoice_response.expiry
        lookup_invoice_response = self.lightning_client.lookup_invoice(preimage_hash.hex())
        invoice_time = lookup_invoice_response.creation_date
        invoice_expiry = lookup_invoice_response.expiry
        # Save the incoming potential payment in the databse.
        return SentOffer(
            sent_offer_id=None,
            squeak_hash=squeak_hash,
            preimage_hash=preimage_hash.hex(),
            preimage=preimage.hex(),
            price_msat=self.price_msat,
            payment_request=invoice_payment_request,
            invoice_time=invoice_time,
            invoice_expiry=invoice_expiry,
            client_addr=client_addr,
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
        return self.squeak_db.insert_profile(squeak_profile)

    def create_contact_profile(self, profile_name, squeak_address):
        address_validator = SqueakAddressValidator()
        if not address_validator.validate(squeak_address):
            raise Exception("Invalid squeak address: {}".format(squeak_address))
        squeak_profile = SqueakProfile(
            profile_id=None,
            profile_name=profile_name,
            private_key=None,
            address=squeak_address,
            sharing=False,
            following=False,
        )
        return self.squeak_db.insert_profile(squeak_profile)

    def get_signing_profiles(self):
        return self.squeak_db.get_signing_profiles()

    def get_contact_profiles(self):
        return self.squeak_db.get_contact_profiles()

    def get_squeak_profile(self, profile_id):
        return self.squeak_db.get_profile(profile_id)

    def get_squeak_profile_by_address(self, address):
        return self.squeak_db.get_profile_by_address(address)

    def get_squeak_profile_by_name(self, name):
        return self.squeak_db.get_profile_by_name(name)

    def set_squeak_profile_following(self, profile_id, following):
        self.squeak_db.set_profile_following(profile_id, following)
        self.squeak_whitelist.refresh()

    def set_squeak_profile_sharing(self, profile_id, sharing):
        self.squeak_db.set_profile_sharing(profile_id, sharing)

    def delete_squeak_profile(self, profile_id):
        self.squeak_db.delete_profile(profile_id)

    def make_squeak(self, profile_id, content_str, replyto_hash):
        squeak_profile = self.squeak_db.get_profile(profile_id)
        squeak_maker = SqueakMaker(self.blockchain_client)
        squeak = squeak_maker.make_squeak(squeak_profile, content_str, replyto_hash)
        return self.save_created_squeak(squeak)

    def get_squeak_entry_with_profile(self, squeak_hash):
        return self.squeak_store.get_squeak_entry_with_profile(squeak_hash)

    def get_followed_squeak_entries_with_profile(self):
        return self.squeak_store.get_followed_squeak_entries_with_profile()

    def get_squeak_entries_with_profile_for_address(
        self, address, min_block, max_block
    ):
        return self.squeak_store.get_squeak_entries_with_profile_for_address(
            address,
            min_block,
            max_block,
        )

    def get_ancestor_squeak_entries_with_profile(self, squeak_hash_str):
        return self.squeak_store.get_ancestor_squeak_entries_with_profile(
            squeak_hash_str,
        )

    def delete_squeak(self, squeak_hash):
        num_deleted_offers = self.squeak_db.delete_offers_for_squeak(squeak_hash)
        logger.info("Deleted number of offers : {}".format(num_deleted_offers))
        return self.squeak_store.delete_squeak(squeak_hash)

    def create_peer(self, peer_name, host, port):
        squeak_peer = SqueakPeer(
            peer_id=None,
            peer_name=peer_name,
            host=host,
            port=port,
            uploading=False,
            downloading=False,
        )
        return self.squeak_db.insert_peer(squeak_peer)

    def get_peer(self, peer_id):
        return self.squeak_db.get_peer(peer_id)

    def get_peers(self):
        return self.squeak_db.get_peers()

    def set_peer_downloading(self, peer_id, downloading):
        self.squeak_db.set_peer_downloading(peer_id, downloading)

    def set_peer_uploading(self, peer_id, uploading):
        self.squeak_db.set_peer_uploading(peer_id, uploading)

    def delete_peer(self, peer_id):
        self.squeak_db.delete_peer(peer_id)

    def get_buy_offers_with_peer(self, squeak_hash):
        return self.squeak_db.get_offers_with_peer(squeak_hash)

    def get_buy_offer_with_peer(self, offer_id):
        return self.squeak_db.get_offer_with_peer(offer_id)

    def pay_offer(self, offer_id):
        # Get the offer from the database
        offer_with_peer = self.squeak_db.get_offer_with_peer(offer_id)
        offer = offer_with_peer.offer

        # Pay the invoice
        payment = self.lightning_client.pay_invoice_sync(offer.payment_request)
        preimage = payment.payment_preimage

        if not preimage:
            raise Exception("Payment failed with error: {}".format(payment.payment_error))

        # Check if preimage is valid
        preimage_hash = sha256(preimage).hexdigest()
        is_valid_preimage = (preimage_hash == offer.payment_hash)

        # Save the preimage of the sent payment
        sent_payment = SentPayment(
            sent_payment_id=None,
            offer_id=offer_id,
            peer_id=offer.peer_id,
            squeak_hash=offer.squeak_hash,
            preimage_hash=offer.payment_hash,
            preimage=preimage.hex(),
            price_msat=offer.price_msat,
            node_pubkey=offer.destination,
            preimage_is_valid=is_valid_preimage,
            time_ms=None,
        )
        sent_payment_id = self.squeak_db.insert_sent_payment(sent_payment)

        if is_valid_preimage:
            self.unlock_squeak(offer, preimage)

        return sent_payment_id

    def unlock_squeak(self, offer, preimage):
        squeak_entry = self.squeak_db.get_squeak_entry(offer.squeak_hash)
        squeak = squeak_entry.squeak

        # Verify with the payment preimage and decryption key ciphertext
        decryption_key_cipher_bytes = offer.key_cipher
        iv = offer.iv
        encrypted_decryption_key = CEncryptedDecryptionKey.from_bytes(
            decryption_key_cipher_bytes
        )

        # Decrypt the decryption key
        decryption_key = encrypted_decryption_key.get_decryption_key(preimage, iv)
        serialized_decryption_key = decryption_key.get_bytes()

        # Check the decryption key
        squeak.SetDecryptionKey(serialized_decryption_key)
        CheckSqueak(squeak)

        # Set the decryption key in the database
        self.squeak_store.unlock_squeak(
            offer.squeak_hash,
            serialized_decryption_key,
        )

    def sync_squeaks(self):
        return self.squeak_sync_controller.sync_timeline()

    def sync_squeak(self, squeak_hash):
        peers = self.squeak_db.get_peers()
        return self.squeak_sync_controller.sync_single_squeak(squeak_hash, peers)

    def get_sent_payments(self):
        return self.squeak_db.get_sent_payments()

    def get_sent_payment(self, sent_payment_id):
        return self.squeak_db.get_sent_payment(sent_payment_id)

    def get_sent_offers(self):
        return self.squeak_db.get_sent_offers()

    def get_received_payments(self):
        return self.squeak_db.get_received_payments()

    def delete_all_expired_offers(self):
        logger.debug("Deleting expired offers.")
        num_expired_offers = self.squeak_db.delete_expired_offers()
        if num_expired_offers > 0:
            logger.info("Deleted number of offers: {}".format(num_expired_offers))

    def verify_all_unverified_squeaks(self):
        self.squeak_block_verifier.verify_all_unverified_squeaks()

    def verify_from_queue(self):
        self.squeak_block_verifier.verify_from_queue()

    def process_subscribed_invoices(self):
        self.sent_offers_verifier.process_subscribed_invoices()
