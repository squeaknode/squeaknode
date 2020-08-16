import logging
import queue

logger = logging.getLogger(__name__)


class SqueakExpiredOfferCleaner:
    def __init__(self, postgres_db):
        self.postgres_db = postgres_db

    def delete_all_expired_offers(self):
        logger.info("Calling delete expired offers.")
        num_expired_offers = self.postgres_db.delete_expired_offers()
        logger.info("Deleted number of offers: {}".format(num_expired_offers))
