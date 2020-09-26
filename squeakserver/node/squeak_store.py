import logging

logger = logging.getLogger(__name__)


class SqueakStore:
    def __init__(
        self, postgres_db, squeak_block_verifier, squeak_rate_limiter, squeak_whitelist
    ):
        self.postgres_db = postgres_db
        self.squeak_block_verifier = squeak_block_verifier
        self.squeak_rate_limiter = squeak_rate_limiter
        self.squeak_whitelist = squeak_whitelist

    def save_uploaded_squeak(self, squeak):
        if not self.squeak_whitelist.should_allow_squeak(squeak):
            raise Exception("Squeak upload not allowed by whitelist.")

        if not self.squeak_rate_limiter.should_rate_limit_allow(squeak):
            raise Exception("Excedeed allowed number of squeaks per block.")

        inserted_squeak_hash = self.postgres_db.insert_squeak(squeak)
        self.squeak_block_verifier.add_squeak_to_queue(inserted_squeak_hash)
        return inserted_squeak_hash

    def save_downloaded_squeak(self, squeak):
        if not self.squeak_rate_limiter.should_rate_limit_allow(squeak):
            raise Exception("Excedeed allowed number of squeaks per block.")

        inserted_squeak_hash = self.postgres_db.insert_squeak(squeak)
        # self.squeak_block_verifier.add_squeak_to_queue(inserted_squeak_hash)
        # Slow operation because of blockchain lookup
        self.squeak_block_verifier.verify_squeak_block(inserted_squeak_hash)
        return inserted_squeak_hash

    def save_created_squeak(self, squeak):
        inserted_squeak_hash = self.postgres_db.insert_squeak(squeak)
        # Slow operation because of blockchain lookup
        self.squeak_block_verifier.verify_squeak_block(inserted_squeak_hash)
        return inserted_squeak_hash

    def get_squeak(self, squeak_hash):
        return self.postgres_db.get_squeak_entry(squeak_hash)

    def get_public_squeak(self, squeak_hash):
        squeak_entry = self.postgres_db.get_squeak_entry(squeak_hash)
        if squeak_entry is None:
            return None
        squeak = squeak_entry.squeak
        # Remove the decryption key before returning.
        squeak.ClearDecryptionKey()
        return squeak

    def get_squeak_entry_with_profile(self, squeak_hash):
        return self.postgres_db.get_squeak_entry_with_profile(squeak_hash)

    def get_followed_squeak_entries_with_profile(self):
        return self.postgres_db.get_followed_squeak_entries_with_profile()

    def get_squeak_entries_with_profile_for_address(
        self, address, min_block, max_block
    ):
        return self.postgres_db.get_squeak_entries_with_profile_for_address(
            address,
            min_block,
            max_block,
        )

    def get_ancestor_squeak_entries_with_profile(self, squeak_hash_str):
        return self.postgres_db.get_thread_ancestor_squeak_entries_with_profile(
            squeak_hash_str,
        )

    def delete_squeak(self, squeak_hash):
        return self.postgres_db.delete_squeak(squeak_hash)

    def lookup_squeaks(self, addresses, min_block, max_block):
        return self.postgres_db.lookup_squeaks(
            addresses,
            min_block,
            max_block,
        )

    def lookup_squeaks_include_locked(self, addresses, min_block, max_block):
        return self.postgres_db.lookup_squeaks(
            addresses,
            min_block,
            max_block,
            include_locked=True,
        )

    def lookup_squeaks_needing_offer(self, addresses, min_block, max_block, peer_id):
        return self.postgres_db.lookup_squeaks_needing_offer(
            addresses,
            min_block,
            max_block,
            peer_id,
        )
