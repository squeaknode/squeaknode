import logging
import threading

logger = logging.getLogger(__name__)


CLEAN_INTERVAL_S = 10.0


class SqueakOfferExpiryWorker:
    def __init__(
        self,
        squeak_controller,
        clean_interval_s=CLEAN_INTERVAL_S,
    ):
        self.squeak_controller = squeak_controller
        self.clean_interval_s = clean_interval_s

    def start_running(self):
        threading.Timer(self.clean_interval_s, self.start_running).start()
        self.remove_expired_offers()

    def remove_expired_offers(self):
        self.squeak_controller.delete_all_expired_offers()
        self.squeak_controller.delete_all_expired_sent_offers()
