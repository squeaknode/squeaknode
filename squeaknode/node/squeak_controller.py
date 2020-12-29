import logging

from squeak.core import CheckSqueak
from squeak.core.signing import CSigningKey
from squeak.core.signing import CSqueakAddress

from squeaknode.core.buy_offer import BuyOffer
from squeaknode.core.sent_offer import SentOffer
from squeaknode.core.sent_payment import SentPayment
from squeaknode.core.squeak_address_validator import SqueakAddressValidator
from squeaknode.core.squeak_peer import SqueakPeer
from squeaknode.core.squeak_profile import SqueakProfile
from squeaknode.core.util import add_tweak
from squeaknode.core.util import generate_tweak
from squeaknode.core.util import subtract_tweak
from squeaknode.node.received_payments_subscription_client import (
    OpenReceivedPaymentsSubscriptionClient,
)
from squeaknode.node.sent_offers_verifier import SentOffersVerifier
from squeaknode.node.squeak_block_verifier import SqueakBlockVerifier
from squeaknode.node.squeak_maker import SqueakMaker
from squeaknode.node.squeak_rate_limiter import SqueakRateLimiter
from squeaknode.node.squeak_store import SqueakStore
from squeaknode.node.squeak_sync_status import SqueakSyncController
from squeaknode.node.squeak_whitelist import SqueakWhitelist

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
        self.squeak_block_verifier = SqueakBlockVerifier(blockchain_client)
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
        return self.squeak_store.save_squeak(squeak, skip_whitelist_check=True)

    def get_public_squeak(self, squeak_hash):
        return self.squeak_store.get_squeak(squeak_hash, clear_decryption_key=True)

    # def get_squeak_entry(self, squeak_hash):
    #     return self.squeak_store.get_squeak(squeak_hash)

    def lookup_squeaks(self, addresses, min_block, max_block):
        return self.squeak_store.lookup_squeaks(addresses, min_block, max_block)

    def lookup_allowed_addresses(self, addresses):
        return self.squeak_whitelist.get_allowed_addresses(addresses)

    def get_buy_offer(self, squeak_hash, client_addr):
        # Check if there is an existing offer for the hash/client_addr combination
        sent_offer = self.get_saved_sent_offer(squeak_hash, client_addr)
        # Get the lightning network node pubkey
        get_info_response = self.lightning_client.get_info()
        pubkey = get_info_response.identity_pubkey
        # Return the buy offer
        return BuyOffer(
            squeak_hash=squeak_hash,
            price_msat=self.price_msat,
            nonce=sent_offer.nonce,
            payment_request=sent_offer.payment_request,
            pubkey=pubkey,
            host=self.lightning_host_port.host,
            port=self.lightning_host_port.port,
        )

    def create_offer(self, squeak_hash, client_addr):
        # Generate a new random nonce
        nonce = generate_tweak()
        # Get the squeak secret key
        squeak = self.squeak_store.get_squeak(squeak_hash)
        secret_key = squeak.GetDecryptionKey()
        # Calculate the preimage
        # preimage = bxor(nonce, secret_key)
        preimage = add_tweak(secret_key, nonce)
        logger.info(
            "Create offer with secret key: {} nonce: {} preimage: {}".format(
                secret_key, nonce, preimage
            )
        )
        # Create the lightning invoice
        add_invoice_response = self.lightning_client.add_invoice(
            preimage, self.price_msat
        )
        logger.info("add_invoice_response: {}".format(add_invoice_response))
        payment_hash = add_invoice_response.r_hash
        invoice_payment_request = add_invoice_response.payment_request
        # invoice_expiry = add_invoice_response.expiry
        lookup_invoice_response = self.lightning_client.lookup_invoice(
            payment_hash.hex()
        )
        invoice_time = lookup_invoice_response.creation_date
        invoice_expiry = lookup_invoice_response.expiry
        # Save the incoming potential payment in the databse.
        return SentOffer(
            sent_offer_id=None,
            squeak_hash=squeak_hash,
            payment_hash=payment_hash.hex(),
            secret_key=preimage.hex(),
            nonce=nonce,
            price_msat=self.price_msat,
            payment_request=invoice_payment_request,
            invoice_time=invoice_time,
            invoice_expiry=invoice_expiry,
            client_addr=client_addr,
        )

    def get_saved_sent_offer(self, squeak_hash, client_addr):
        # Check if there is an existing offer for the hash/client_addr combination
        sent_offer = self.squeak_db.get_sent_offer_by_squeak_hash_and_client_addr(
            squeak_hash,
            client_addr,
        )
        if sent_offer:
            return sent_offer
        sent_offer = self.create_offer(squeak_hash, client_addr)
        self.squeak_db.insert_sent_offer(sent_offer)
        return sent_offer

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
            raise Exception(
                "Invalid squeak address: {}".format(squeak_address))
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
        squeak = squeak_maker.make_squeak(
            squeak_profile, content_str, replyto_hash)
        return self.save_created_squeak(squeak)

    def get_squeak_entry_with_profile(self, squeak_hash):
        return self.squeak_store.get_squeak_entry_with_profile(squeak_hash)

    def get_timeline_squeak_entries_with_profile(self):
        return self.squeak_store.get_timeline_squeak_entries_with_profile()

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
        num_deleted_offers = self.squeak_db.delete_offers_for_squeak(
            squeak_hash)
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
            raise Exception(
                "Payment failed with error: {}".format(payment.payment_error)
            )

        # Calculate the secret key
        nonce = offer.nonce
        # secret_key = bxor(nonce, preimage)
        secret_key = subtract_tweak(preimage, nonce)
        logger.info(
            "Pay offer with secret key: {} nonce: {} preimage: {}".format(
                secret_key, nonce, preimage
            )
        )

        # Save the preimage of the sent payment
        sent_payment = SentPayment(
            sent_payment_id=None,
            offer_id=offer_id,
            peer_id=offer.peer_id,
            squeak_hash=offer.squeak_hash,
            payment_hash=offer.payment_hash,
            secret_key=secret_key.hex(),
            price_msat=offer.price_msat,
            node_pubkey=offer.destination,
            time_ms=None,
        )
        sent_payment_id = self.squeak_db.insert_sent_payment(sent_payment)

        self.unlock_squeak(offer, secret_key)

        return sent_payment_id

    def unlock_squeak(self, offer, secret_key):
        squeak_entry = self.squeak_db.get_squeak_entry(offer.squeak_hash)
        squeak = squeak_entry.squeak

        # Check the decryption key
        squeak.SetDecryptionKey(secret_key)
        CheckSqueak(squeak)

        # Set the decryption key in the database
        self.squeak_store.unlock_squeak(
            offer.squeak_hash,
            secret_key,
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
            logger.info("Deleted number of offers: {}".format(
                num_expired_offers))

    def delete_all_expired_sent_offers(self):
        logger.debug("Deleting expired sent offers.")
        num_expired_sent_offers = self.squeak_db.delete_expired_offers()
        if num_expired_sent_offers > 0:
            logger.info(
                "Deleted number of sent offers: {}".format(
                    num_expired_sent_offers)
            )

    def process_subscribed_invoices(self):
        self.sent_offers_verifier.process_subscribed_invoices()

    def subscribe_received_payments(self, initial_index):
        with OpenReceivedPaymentsSubscriptionClient(
            self.squeak_db,
            initial_index,
        ) as client:
            for payment in client.get_received_payments():
                yield payment
