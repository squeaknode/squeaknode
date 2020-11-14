import logging
import threading

logger = logging.getLogger(__name__)


class SqueakBlockQueueWorker:
    def __init__(self, squeak_controller):
        self.squeak_controller = squeak_controller

    def start_running(self):
        threading.Thread(target=self.process_queue, daemon=True).start()

    def process_queue(self):
        self.squeak_controller.verify_from_queue()
