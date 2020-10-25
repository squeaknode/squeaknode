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

        try:
            block_info = self._get_block_info_for_height(squeak.nBlockHeight)
        except Exception as e:
            logger.error(
                "Failed to sync because unable to get blockchain info.", exc_info=False
            )
            return

        if squeak.hashBlock.hex() == block_info.block_hash:
            logger.info("block hash correct: {}".format(block_info))
            self._mark_squeak_verified(squeak_hash, block_info)
        else:
            logger.info("block hash incorrect: {}".format(block_info))
            self._delete_squeak(squeak_hash)

    def verify_all_unverified_squeaks(self):
        logger.debug("Verifying all unverified squeaks.")
        squeaks_to_verify = self.postgres_db.get_unverified_block_squeaks()
        for squeak_hash in squeaks_to_verify:
            self.verify_squeak_block(squeak_hash)

    def add_squeak_to_queue(self, squeak_hash):
        self.unverified_queue.put(squeak_hash)

    def verify_from_queue(self):
        while True:
            try:
                squeak_hash = self.unverified_queue.get()
                self.verify_squeak_block(squeak_hash)
            except:
                logger.error("something bad happened", exc_info=True)

    def _get_squeak(self, squeak_hash):
        squeak_entry = self.postgres_db.get_squeak_entry(squeak_hash)
        return squeak_entry.squeak

    def _mark_squeak_verified(self, squeak_hash, block_info):
        block_header_bytes = bytes.fromhex(block_info.block_header)
        self.postgres_db.mark_squeak_block_valid(squeak_hash, block_header_bytes)

    def _delete_squeak(self, squeak_hash):
        self.postgres_db.delete_squeak(squeak_hash)

    def _get_block_info_for_height(self, block_height):
        return self.blockchain_client.get_block_info_by_height(block_height)
