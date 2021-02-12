import logging
import threading

from squeaknode.core.exception import ProcessReceivedPaymentError
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
        self.stopped_permanently = threading.Event()
        self.lock = threading.Lock()

    def start_processing(self):
        with self.lock:
            if self.stopped_permanently.is_set():
                return
            self.stopped.set()
            self.stopped = threading.Event()
            threading.Thread(
                target=self.process_subscribed_invoices,
                args=(self.stopped,),
            ).start()

    def stop_processing(self, permanent=False):
        with self.lock:
            self.stopped.set()
            if permanent:
                self.stopped_permanently.set()

    def process_subscribed_invoices(self, stopped: threading.Event):
        def get_sent_offer_for_payment_hash(payment_hash: bytes) -> SentOffer:
            return self.squeak_db.get_sent_offer_by_payment_hash(
                payment_hash
            )
        while not stopped.is_set():
            try:
                latest_settle_index = self.squeak_db.get_latest_settle_index() or 0
                logger.info(
                    "Processing from settle_index: {}".format(
                        latest_settle_index)
                )
                for received_payment in self.squeak_core.get_received_payments(
                        get_sent_offer_for_payment_hash,
                        latest_settle_index,
                        stopped,
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
            except ProcessReceivedPaymentError:
                logger.error(
                    "Unable to subscribe invoices from lnd. Retrying in "
                    "{} seconds.".format(self.retry_s),
                )
            stopped.wait(self.retry_s)
