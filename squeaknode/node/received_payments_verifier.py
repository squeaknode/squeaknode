import logging
import queue
import time


logger = logging.getLogger(__name__)

LND_CONNECT_RETRY_S = 10


class ReceivedPaymentsVerifier:
    def __init__(self, squeak_db, lightning_client):
        self.squeak_db = squeak_db
        self.lightning_client = lightning_client

    def verify_received_payment(self, invoice):
        logger.info("Verifying invoice: {}".format(invoice))

    def process_subscribed_invoices(self):
        while True:
            try:
                for invoice in self.lightning_client.subscribe_invoices():
                    self.verify_received_payment(invoice)
            except:
                logger.error(
                    "Unable to subscribe invoices from lnd. Retrying in {} seconds".format(LND_CONNECT_RETRY_S),
                    exc_info=True,
                )
                time.sleep(LND_CONNECT_RETRY_S)

    def _mark_received_payment_paid(self, preimage_hash):
        # self.squeak_db.mark_squeak_block_valid(squeak_hash, block_header_bytes)
        pass
