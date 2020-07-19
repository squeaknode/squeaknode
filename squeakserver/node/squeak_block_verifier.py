import logging
import queue
import threading


logger = logging.getLogger(__name__)


class SqueakBlockVerifier:

    def __init__(self, postgres_db, blockchain_client):
        self.postgres_db = postgres_db
        self.blockchain_client = blockchain_client
        self.unverified_queue = queue.Queue()

    def verify_squeak_block(self, squeak_hash):
        logger.info('Verifying squeak hash: {}'.format(squeak_hash))
        squeak = self._get_squeak(squeak_hash)
        block_info = self._get_block_info(squeak)

    def verify_all_unverified_squeaks(self):
        logger.info('Calling verify_squeaks.')
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
        return self.postgres_db.get_squeak(squeak_hash)

    def _mark_squeak_verified(self, squeak_hash):
        # TODO
        pass

    def _get_block_info(self, squeak):
        block_height = squeak.nBlockHeight
        block_hash = self.blockchain_client.get_block_hash(block_height)
        logger.info('Got block hash from blockchain: {}'.format(block_hash))
        logger.info('Got block hash from squeak: {}'.format(squeak.hashBlock))
        logger.info('Is block hash correct: {}'.format(squeak.hashBlock == block_hash))
