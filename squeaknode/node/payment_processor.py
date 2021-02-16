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
        self.stopped = threading.Event()
        self.lock = threading.Lock()

    def start_processing(self):
        with self.lock:
            self.stopped.set()
            self.stopped.clear()
            threading.Thread(
                target=self.process_subscribed_invoices,
            ).start()

    def stop_processing(self):
        with self.lock:
            self.stopped.set()

    def process_subscribed_invoices(self):
        while not self.stopped.is_set():
            try:
                for received_payment in self.squeak_core.get_received_payments(
                        self.get_latest_settle_index(),
                        self.get_sent_offer_for_payment_hash,
                        self.stopped,
                        retry_s=self.retry_s,
                ):
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
                    "Error processing received payments.", exc_info=True)
            self.stopped.wait(self.retry_s)

    def get_latest_settle_index(self):
        return self.squeak_db.get_latest_settle_index() or 0

    def get_sent_offer_for_payment_hash(self, payment_hash: bytes) -> SentOffer:
        return self.squeak_db.get_sent_offer_by_payment_hash(
            payment_hash
        )
