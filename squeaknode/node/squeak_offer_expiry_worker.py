import logging
import threading

from squeaknode.node.squeak_controller import SqueakController


logger = logging.getLogger(__name__)


class SqueakOfferExpiryWorker:
    def __init__(
        self,
        squeak_controller: SqueakController,
        clean_interval_s: int,
    ):
        self.squeak_controller = squeak_controller
        self.clean_interval_s = clean_interval_s

    def start_running(self):
        timer = threading.Timer(
            self.clean_interval_s,
            self.start_running,
        )
        timer.daemon = True
        timer.start()
        self.remove_expired_offers()

    def remove_expired_offers(self):
        self.squeak_controller.delete_all_expired_received_offers()
        self.squeak_controller.delete_all_expired_sent_offers()
