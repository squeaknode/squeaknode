import logging
from typing import List


logger = logging.getLogger(__name__)


class SqueakStore:
    def __init__(
        self, squeak_db, squeak_core, squeak_rate_limiter, squeak_whitelist
    ):
        self.squeak_db = squeak_db
        self.squeak_core = squeak_core
        self.squeak_rate_limiter = squeak_rate_limiter
        self.squeak_whitelist = squeak_whitelist

    # def save_squeak(self, squeak: CSqueak, skip_whitelist_check: bool = False):
    #     if not skip_whitelist_check:
    #         if not self.squeak_whitelist.should_allow_squeak(squeak):
    #             raise Exception("Squeak upload not allowed by whitelist.")

    #         if not self.squeak_rate_limiter.should_rate_limit_allow(squeak):
    #             raise Exception(
    #                 "Excedeed allowed number of squeaks per block.")
    #     block_info = self.squeak_core.validate_squeak(squeak)
    #     inserted_squeak_hash = self.squeak_db.insert_squeak(
    #         squeak, block_info.block_header)
    #     return inserted_squeak_hash

    def get_squeak(self, squeak_hash: bytes, clear_decryption_key: bool = False):
        squeak_entry = self.squeak_db.get_squeak_entry(squeak_hash)
        if squeak_entry is None:
            return None
        squeak = squeak_entry.squeak
        if clear_decryption_key:
            squeak.ClearDecryptionKey()
        return squeak

    def get_squeak_entry_with_profile(self, squeak_hash: bytes):
        return self.squeak_db.get_squeak_entry_with_profile(squeak_hash)

    def get_timeline_squeak_entries_with_profile(self):
        return self.squeak_db.get_timeline_squeak_entries_with_profile()

    def get_squeak_entries_with_profile_for_address(
        self, address: str, min_block: int, max_block: int
    ):
        return self.squeak_db.get_squeak_entries_with_profile_for_address(
            address,
            min_block,
            max_block,
        )

    def get_ancestor_squeak_entries_with_profile(self, squeak_hash: bytes):
        return self.squeak_db.get_thread_ancestor_squeak_entries_with_profile(
            squeak_hash,
        )

    def delete_squeak(self, squeak_hash: bytes):
        return self.squeak_db.delete_squeak(squeak_hash)

    def lookup_squeaks(self, addresses: List[str], min_block: int, max_block: int):
        return self.squeak_db.lookup_squeaks(
            addresses,
            min_block,
            max_block,
        )

    def lookup_squeaks_include_locked(self, addresses: List[str], min_block: int, max_block: int):
        return self.squeak_db.lookup_squeaks(
            addresses,
            min_block,
            max_block,
            include_locked=True,
        )

    def lookup_squeaks_needing_offer(self, addresses: List[str], min_block, max_block, peer_id):
        return self.squeak_db.lookup_squeaks_needing_offer(
            addresses,
            min_block,
            max_block,
            peer_id,
        )

    def unlock_squeak(self, squeak_hash: bytes, secret_key: bytes):
        self.squeak_db.set_squeak_decryption_key(
            squeak_hash,
            secret_key,
        )
