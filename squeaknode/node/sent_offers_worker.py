import logging
import threading

logger = logging.getLogger(__name__)


class SentOffersWorker:
    def __init__(self, squeak_controller):
        self.squeak_controller = squeak_controller

    def start_running(self):
        threading.Thread(
            target=self.process_subscribed_invoices, daemon=True).start()

    def process_subscribed_invoices(self):
        self.squeak_controller.process_subscribed_invoices()
