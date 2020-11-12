import logging
import threading

logger = logging.getLogger(__name__)


class SentOffersWorker:
    def __init__(self, sent_offers_verifier):
        self.sent_offers_verifier = sent_offers_verifier

    def start_running(self):
        threading.Thread(target=self.process_subscribed_invoices, daemon=True).start()

    def process_subscribed_invoices(self):
        self.sent_offers_verifier.process_subscribed_invoices()
