import logging
import threading


logger = logging.getLogger(__name__)


class SqueakBlockQueueWorker:

    def __init__(self, squeak_block_verifier):
        self.squeak_block_verifier = squeak_block_verifier

    def start_running(self):
        threading.Thread(target=self.process_queue, daemon=True).start()

    def process_queue(self):
        self.squeak_block_verifier.verify_from_queue()
