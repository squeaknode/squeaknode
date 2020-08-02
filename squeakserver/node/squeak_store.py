import logging

logger = logging.getLogger(__name__)


class SqueakStore:
    def __init__(self, postgres_db, squeak_block_verifier, squeak_rate_limiter, squeak_whitelist):
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

    def save_created_squeak(self, squeak):
        inserted_squeak_hash = self.postgres_db.insert_squeak(squeak)
        self.squeak_block_verifier.verify_squeak_block(inserted_squeak_hash)
        return inserted_squeak_hash
