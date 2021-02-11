import logging
import threading

logger = logging.getLogger(__name__)


class SentOffersWorker:
    def __init__(self, payment_processor, stopped: threading.Event):
        self.payment_processor = payment_processor
        self.stopped = stopped

    def start_running(self):
        threading.Thread(
            target=self.process_subscribed_invoices,
            # daemon=True,
        ).start()

    def process_subscribed_invoices(self):
        logger.info("Starting SentOffersWorker...")
        self.payment_processor.start_processing()
        self.stopped.wait()
        logger.info("Stopping SentOffersWorker...")
        self.payment_processor.stop_processing(permanent=True)
