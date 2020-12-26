import logging

from squeaknode.node.sent_offers_worker import SentOffersWorker
from squeaknode.node.squeak_offer_expiry_worker import SqueakOfferExpiryWorker
from squeaknode.node.squeak_peer_sync_worker import SqueakPeerSyncWorker

logger = logging.getLogger(__name__)


class SqueakNode:
    def __init__(
        self,
        squeak_controller,
        sync_interval_s,
    ):
        self.squeak_controller = squeak_controller
        self.squeak_peer_sync_worker = SqueakPeerSyncWorker(
            self.squeak_controller,
            sync_interval_s,
        )
        self.squeak_offer_expiry_worker = SqueakOfferExpiryWorker(
            self.squeak_controller,
        )
        self.sent_offers_worker = SentOffersWorker(
            self.squeak_controller,
        )

    def start_running(self):
        self.squeak_peer_sync_worker.start_running()
        self.squeak_offer_expiry_worker.start_running()
        self.sent_offers_worker.start_running()
