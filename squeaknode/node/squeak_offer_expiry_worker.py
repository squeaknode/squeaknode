import logging

from squeaknode.node.periodic_worker import PeriodicWorker
from squeaknode.node.squeak_controller import SqueakController


logger = logging.getLogger(__name__)


class SqueakOfferExpiryWorker(PeriodicWorker):
    def __init__(
        self,
        squeak_controller: SqueakController,
        clean_interval_s: int,
    ):
        self.squeak_controller = squeak_controller
        self.clean_interval_s = clean_interval_s

    def work_fn(self):
        self.squeak_controller.delete_all_expired_received_offers()
        self.squeak_controller.delete_all_expired_sent_offers()

    def get_interval_s(self):
        return self.clean_interval_s

    def get_name(self):
        return "offer_expiry_worker"
