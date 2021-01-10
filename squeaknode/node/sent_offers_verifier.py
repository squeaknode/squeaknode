import logging

from squeaknode.core.sent_offer import SentOffer


logger = logging.getLogger(__name__)

LND_CONNECT_RETRY_S = 10


class SentOffersVerifier:
    def __init__(self, squeak_db, squeak_core):
        self.squeak_db = squeak_db
        self.squeak_core = squeak_core

    def process_subscribed_invoices(self):
        while True:
            self.try_processing()

    def try_processing(self):
        latest_settle_index = self._get_latest_settle_index() or 0

        def get_sent_offer_for_payment_hash(payment_hash: bytes) -> SentOffer:
            return self.squeak_db.get_sent_offer_by_payment_hash(
                payment_hash
            )

        for received_payment in self.squeak_core.get_received_payments(
                get_sent_offer_for_payment_hash,
                latest_settle_index,
                LND_CONNECT_RETRY_S,
        ):
            self.squeak_db.insert_received_payment(received_payment)

    def _get_latest_settle_index(self):
        logger.info("Getting latest settle index from db...")
        return self.squeak_db.get_latest_settle_index()
