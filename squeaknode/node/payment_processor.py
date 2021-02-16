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
        self._cancel_fn = None

    def start_processing(self):
        with self.lock:
            self.stopped.set()
            self._cancel_subscription()
            self.stopped.clear()
            threading.Thread(
                target=self._process_subscribed_invoices,
            ).start()

    def stop_processing(self):
        with self.lock:
            self.stopped.set()
            self._cancel_subscription()

    def _cancel_subscription(self):
        logger.info("Cancelling subscription...")
        if self._cancel_fn is not None:
            self._cancel_fn()
            logger.info("Cancelled subscription.")

    def _process_subscribed_invoices(self):
        received_payments_result = self.squeak_core.get_received_payments(
            self.get_latest_settle_index(),
            self.get_sent_offer_for_payment_hash,
        )
        self._cancel_fn = received_payments_result.cancel_fn
        for received_payment in received_payments_result.result_stream:
            logger.info(
                "Got received payment: {}".format(received_payment))
            try:
                self.squeak_db.insert_received_payment(received_payment)
            except DuplicateReceivedPaymentError:
                pass
            # self.squeak_db.delete_sent_offer(received_payment.payment_hash)

    def get_sent_offer_for_payment_hash(self, payment_hash: bytes) -> SentOffer:
        logger.info("Current sent offers: {}".format(
            self.squeak_db.get_sent_offers(),
        ))
        logger.info("Getting sent offer for payment hash: {}".format(
            payment_hash.hex(),
        ))
        sent_offer = self.squeak_db.get_sent_offer_by_payment_hash(
            payment_hash
        )
        logger.info("Got sent offer: {}".format(
            sent_offer,
        ))
        return sent_offer

    def get_latest_settle_index(self) -> int:
        return self.squeak_db.get_latest_settle_index() or 0
