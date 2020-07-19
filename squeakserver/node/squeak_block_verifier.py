import logging
import queue

logger = logging.getLogger(__name__)


class SqueakBlockVerifier:
    def __init__(self, postgres_db, blockchain_client):
        self.postgres_db = postgres_db
        self.blockchain_client = blockchain_client
        self.unverified_queue = queue.Queue()

    def verify_squeak_block(self, squeak_hash):
        logger.info("Verifying squeak hash: {}".format(squeak_hash))
        squeak = self._get_squeak(squeak_hash)
        valid_block_info = self._check_block_info(squeak)
        logger.info("Is block hash correct: {}".format(valid_block_info))
        if valid_block_info:
            block_header = self._get_block_header(squeak)
            self._mark_squeak_verified(squeak_hash, block_header)
        else:
            self._delete_squeak

    def verify_all_unverified_squeaks(self):
        logger.info("Calling verify_squeaks.")
        squeaks_to_verify = self.postgres_db.get_unverified_block_squeaks()
        for squeak_hash in squeaks_to_verify:
            self.verify_squeak_block(squeak_hash)

    def add_squeak_to_queue(self, squeak_hash):
        self.unverified_queue.put(squeak_hash)

    def verify_from_queue(self):
        while True:
            squeak_hash = self.unverified_queue.get()
            self.verify_squeak_block(squeak_hash)

    def _get_squeak(self, squeak_hash):
        squeak_entry = self.postgres_db.get_squeak_entry(squeak_hash)
        return squeak_entry.squeak

    def _mark_squeak_verified(self, squeak_hash, block_header):
        self.postgres_db.mark_squeak_block_valid(squeak_hash, block_header)

    def _delete_squeak(self, squeak_hash):
        self.postgres_db.delete_squeak(squeak_hash)

    def _check_block_info(self, squeak):
        block_height = squeak.nBlockHeight
        block_hash = self._get_block_hash(block_height)
        return squeak.hashBlock == block_hash

    def _get_block_header(self, squeak):
        block_hash_str = squeak.hashBlock.hex()
        block_header = self.blockchain_client.get_block_header(block_hash_str, False)
        logger.info("Got block header from blockchain: {}".format(block_header))
        return bytes.fromhex(block_header)

    def _get_block_hash(self, block_height):
        block_hash = self.blockchain_client.get_block_hash(block_height)
        logger.info("Got block hash from blockchain: {}".format(block_hash))
        return block_hash
