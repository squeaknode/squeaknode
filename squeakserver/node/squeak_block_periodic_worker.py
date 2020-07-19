import logging
import threading
import time


logger = logging.getLogger(__name__)


VERIFY_UPDATE_INTERVAL_S = 10.0


class SqueakBlockPeriodicWorker:

    def __init__(self, squeak_block_verifier):
        self.squeak_block_verifier = squeak_block_verifier

    def start_running(self):
        threading.Timer(VERIFY_UPDATE_INTERVAL_S, self.start_running).start()
        self.squeak_block_verifier.verify_all_unverified_squeaks()

