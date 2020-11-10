import logging

logger = logging.getLogger(__name__)


class SqueakExpiredOfferCleaner:
    def __init__(self, squeak_db):
        self.squeak_db = squeak_db

    def delete_all_expired_offers(self):
        logger.debug("Deleting expired offers.")
        num_expired_offers = self.squeak_db.delete_expired_offers()
        if num_expired_offers > 0:
            logger.info("Deleted number of offers: {}".format(num_expired_offers))
