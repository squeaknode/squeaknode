import logging
import threading

from squeaknode.core.sent_offer import SentOffer
from squeaknode.db.exception import DuplicateReceivedPaymentError


logger = logging.getLogger(__name__)


class PaymentProcessor:

    def __init__(
        self,
        squeak_db,
        squeak_core,
        retry_s: int = 10,
    ):
        self.squeak_db = squeak_db
        self.squeak_core = squeak_core
        self.retry_s = retry_s
        self.lock = threading.Lock()
        self.current_task = None

    def start_processing(self):
        with self.lock:
            if self.current_task is not None:
                self.current_task.stop_processing()
            self.current_task = PaymentProcessorTask(
                self.squeak_db,
                self.squeak_core,
                self.retry_s,
            )
            self.current_task.start_processing()

    def stop_processing(self):
        with self.lock:
            if self.current_task is not None:
                self.current_task.stop_processing()


class PaymentProcessorTask:

    def __init__(
        self,
        squeak_db,
        squeak_core,
        retry_s: int,
    ):
        self.squeak_db = squeak_db
        self.squeak_core = squeak_core
        self.retry_s = retry_s
        self.stopped = threading.Event()
        self.payments_result = None

    def start_processing(self):
        logger.info("Starting payment processor task.")
        threading.Thread(
            target=self.process_subscribed_invoices,
        ).start()

    def stop_processing(self):
        logger.info("Stopping payment processor task.")
        self.stopped.set()
        if self.payments_result is not None:
            self.payments_result.cancel_fn()

    def process_subscribed_invoices(self):
        while not self.stopped.is_set():
            try:
                latest_settle_index = self.get_latest_settle_index()
                logger.info("Starting payment subscription with settle index: {}".format(
                    latest_settle_index,
                ))
                self.payments_result = self.squeak_core.get_received_payments(
                    latest_settle_index,
                    self.get_sent_offer_for_payment_hash,
                )

                if self.stopped.is_set():
                    self.payments_result.cancel_fn()

                for received_payment in self.payments_result.result_stream:
                    logger.info(
                        "Got received payment: {}".format(received_payment))
                    try:
                        self.squeak_db.insert_received_payment(
                            received_payment)
                    except DuplicateReceivedPaymentError:
                        pass
                    self.squeak_db.delete_sent_offer(
                        received_payment.payment_hash)
            except Exception:
                logger.error(
                    "Error processing received payments. Retrying in {} seconds.".format(
                        self.retry_s),
                )
            self.stopped.wait(self.retry_s)

    def get_latest_settle_index(self):
        return self.squeak_db.get_latest_settle_index() or 0

    def get_sent_offer_for_payment_hash(self, payment_hash: bytes) -> SentOffer:
        return self.squeak_db.get_sent_offer_by_payment_hash(
            payment_hash
        )
