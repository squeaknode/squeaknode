import logging
import threading

logger = logging.getLogger(__name__)


class ProcessReceivedPaymentsWorker:
    def __init__(self, payment_processor):
        self.payment_processor = payment_processor
        self.stopped = threading.Event()

    def start_running(self):
        threading.Thread(
            target=self.process_subscribed_invoices,
            # daemon=True,
            name="process_received_payments_thread",
        ).start()

    def stop_running(self):
        self.stopped.set()

    def process_subscribed_invoices(self):
        logger.info("Starting ProcessReceivedPaymentsWorker...")
        self.payment_processor.start_processing()
        self.stopped.wait()
        logger.info("Stopping ProcessReceivedPaymentsWorker...")
        self.payment_processor.stop_processing()
