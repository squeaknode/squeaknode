import logging
import threading

logger = logging.getLogger(__name__)


CLEAN_INTERVAL_S = 10.0


class SqueakOfferExpiryWorker:
    def __init__(
        self,
        squeak_expired_offer_cleaner,
        clean_interval_s=CLEAN_INTERVAL_S,
    ):
        self.squeak_expired_offer_cleaner = squeak_expired_offer_cleaner
        self.clean_interval_s = clean_interval_s

    def start_running(self):
        threading.Timer(self.clean_interval_s, self.start_running).start()
        self.remove_expired_offers()

    def remove_expired_offers(self):
        self.squeak_expired_offer_cleaner.delete_all_expired_offers()
