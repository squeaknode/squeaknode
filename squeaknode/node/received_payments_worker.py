import logging
import threading

logger = logging.getLogger(__name__)


class ReceivedPaymentsWorker:
    def __init__(self, received_payments_verifier):
        self.received_payments_verifier = received_payments_verifier

    def start_running(self):
        threading.Thread(target=self.process_subscribed_invoices, daemon=True).start()

    def process_subscribed_invoices(self):
        self.received_payments_verifier.process_subscribed_invoices()
