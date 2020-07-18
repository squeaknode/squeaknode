import logging


logger = logging.getLogger(__name__)


class SqueakBlockVerifier:

    def __init__(self, postgres_db, blockchain_client):
        self.postgres_db = postgres_db
        self.blockchain_client = blockchain_client

    def verify_squeak_block(self, squeak_hash):
        logger.info('Verifying squeak hash: {}'.format(squeak_hash))
