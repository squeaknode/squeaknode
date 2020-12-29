import logging
import time

from squeaknode.core.received_payment import ReceivedPayment

logger = logging.getLogger(__name__)

LND_CONNECT_RETRY_S = 10


class SentOffersVerifier:
    def __init__(self, squeak_db, lightning_client):
        self.squeak_db = squeak_db
        self.lightning_client = lightning_client

    def verify_sent_offer(self, invoice):
        logger.info("Verifying invoice: {}".format(invoice))
        if invoice.settled:
            payment_hash = invoice.r_hash.hex()
            settle_index = invoice.settle_index
            self._record_payment(payment_hash, settle_index)

    def process_subscribed_invoices(self):
        while True:
            self.try_processing()

    def try_processing(self):
        latest_settle_index = self._get_latest_settle_index() or 0
        logger.info("latest settle index: {}".format(latest_settle_index))
        try:
            for invoice in self.lightning_client.subscribe_invoices(
                settle_index=latest_settle_index,
            ):
                self.verify_sent_offer(invoice)
        except Exception:
            logger.info(
                "Unable to subscribe invoices from lnd. Retrying in "
                "{} seconds.".format(LND_CONNECT_RETRY_S),
            )
            time.sleep(LND_CONNECT_RETRY_S)

    def _get_latest_settle_index(self):
        logger.info("Getting latest settle index from db...")
        return self.squeak_db.get_latest_settle_index()

    def _record_payment(self, payment_hash, settle_index):
        logger.info(
            "Saving received payment for payment_hash: {} with settle_index: {}".format(
                payment_hash,
                settle_index,
            )
        )
        sent_offer = self.squeak_db.get_sent_offer_by_payment_hash(
            payment_hash)
        received_payment = ReceivedPayment(
            received_payment_id=None,
            created=None,
            squeak_hash=sent_offer.squeak_hash,
            payment_hash=sent_offer.payment_hash,
            price_msat=sent_offer.price_msat,
            settle_index=settle_index,
            client_addr=sent_offer.client_addr,
        )
        self.squeak_db.insert_received_payment(received_payment)
