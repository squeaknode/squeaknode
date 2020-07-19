import logging
import threading
import time


logger = logging.getLogger(__name__)


VERIFY_UPDATE_INTERVAL_S = 10.0


class SqueakBlockPeriodicWorker:

    def __init__(self, squeak_block_verifier, postgres_db):
        self.squeak_block_verifier = squeak_block_verifier
        self.postgres_db = postgres_db

    def verify_squeaks(self):
        logger.info('Calling verify_squeaks.')
        squeaks_to_verify = self.postgres_db.get_unverified_block_squeaks()
        for squeak_hash in squeaks_to_verify:
            self.squeak_block_verifier.verify_squeak_block(squeak_hash)

    def start_running(self):
        threading.Timer(VERIFY_UPDATE_INTERVAL_S, self.start_running).start()
        self.verify_squeaks()
