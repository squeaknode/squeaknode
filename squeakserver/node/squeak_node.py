from squeak.core.encryption import (
    CEncryptedDecryptionKey,
    generate_initialization_vector,
)
from squeak.core.signing import CSigningKey, CSqueakAddress

from squeakserver.core.squeak_address_validator import SqueakAddressValidator
from squeakserver.node.squeak_block_periodic_worker import SqueakBlockPeriodicWorker
from squeakserver.node.squeak_block_queue_worker import SqueakBlockQueueWorker
from squeakserver.node.squeak_block_verifier import SqueakBlockVerifier
from squeakserver.node.squeak_maker import SqueakMaker
from squeakserver.node.squeak_rate_limiter import SqueakRateLimiter
from squeakserver.node.squeak_whitelist import SqueakWhitelist
from squeakserver.server.buy_offer import BuyOffer
from squeakserver.server.squeak_profile import SqueakProfile
from squeakserver.server.squeak_subscription import SqueakSubscription
from squeakserver.server.util import generate_offer_preimage


class SqueakNode:
    def __init__(
        self,
        postgres_db,
        blockchain_client,
        lightning_client,
        lightning_host_port,
        price,
        max_squeaks_per_address_per_hour,
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
        self.squeak_rate_limiter = SqueakRateLimiter(
            postgres_db,
            blockchain_client,
            lightning_client,
            max_squeaks_per_address_per_hour,
        )
        self.squeak_whitelist = SqueakWhitelist(postgres_db,)

    def start_running(self):
        # self.squeak_block_periodic_worker.start_running()
        self.squeak_block_queue_worker.start_running()

    def save_squeak(self, squeak):
        if not self.squeak_whitelist.should_allow_squeak(squeak):
            raise Exception("Squeak upload not allowed by whitelist.")

        if not self.squeak_rate_limiter.should_rate_limit_allow(squeak):
            raise Exception("Excedeed allowed number of squeaks per block.")

        inserted_squeak_hash = self.postgres_db.insert_squeak(squeak)
        self.squeak_block_verifier.add_squeak_to_queue(inserted_squeak_hash)
        return inserted_squeak_hash

    def save_squeak_and_verify(self, squeak):
        if not self.squeak_rate_limiter.should_rate_limit_allow(squeak):
            raise Exception("Excedeed allowed number of squeaks per block.")

        inserted_squeak_hash = self.postgres_db.insert_squeak(squeak)
        self.squeak_block_verifier.verify_squeak_block(inserted_squeak_hash)
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
            whitelisted=False,
        )
        return self.postgres_db.insert_profile(squeak_profile)

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
            whitelisted=False,
        )
        return self.postgres_db.insert_profile(squeak_profile)

    def get_signing_profiles(self):
        return self.postgres_db.get_signing_profiles()

    def get_contact_profiles(self):
        return self.postgres_db.get_contact_profiles()

    def get_squeak_profile(self, profile_id):
        return self.postgres_db.get_profile(profile_id)

    def get_squeak_profile_by_address(self, address):
        return self.postgres_db.get_profile_by_address(address)

    def set_squeak_profile_whitelisted(self, profile_id, whitelisted):
        self.postgres_db.set_profile_whitelisted(profile_id, whitelisted)
        self.squeak_whitelist.refresh()

    def set_squeak_profile_following(self, profile_id, following):
        self.postgres_db.set_profile_following(profile_id, following)

    def set_squeak_profile_sharing(self, profile_id, sharing):
        self.postgres_db.set_profile_sharing(profile_id, sharing)

    def make_squeak(self, profile_id, content_str, replyto_hash):
        squeak_profile = self.postgres_db.get_profile(profile_id)
        squeak_maker = SqueakMaker(self.lightning_client)
        squeak = squeak_maker.make_squeak(squeak_profile, content_str, replyto_hash)
        return self.save_squeak_and_verify(squeak)

    def get_squeak_entry_with_profile(self, squeak_hash):
        return self.postgres_db.get_squeak_entry_with_profile(squeak_hash)

    def get_followed_squeak_entries_with_profile(self):
        return self.postgres_db.get_followed_squeak_entries_with_profile()

    def get_squeak_entries_with_profile_for_address(
        self, address, min_block, max_block
    ):
        return self.postgres_db.get_squeak_entries_with_profile_for_address(
            address, min_block, max_block,
        )

    def get_ancestor_squeak_entries_with_profile(self, squeak_hash_str):
        return self.postgres_db.get_thread_ancestor_squeak_entries_with_profile(
            squeak_hash_str,
        )

    def delete_squeak(self, squeak_hash):
        return self.postgres_db.delete_squeak(squeak_hash)

    def create_subscription(self, subscription_name, host, port):
        squeak_subscription = SqueakSubscription(
            subscription_id=None,
            subscription_name=subscription_name,
            host=host,
            port=port,
            publishing=False,
            subscribed=False,
        )
        return self.postgres_db.insert_subscription(squeak_subscription)

    def get_subscription(self, subscription_id):
        return self.postgres_db.get_subscription(subscription_id)

    def get_subscriptions(self):
        return self.postgres_db.get_subscriptions()

    def set_subscription_subscribed(self, subscription_id, subscribed):
        self.postgres_db.set_subscription_subscribed(subscription_id, subscribed)

    def set_subscription_publishing(self, subscription_id, publishing):
        self.postgres_db.set_subscription_publishing(subscription_id, publishing)
