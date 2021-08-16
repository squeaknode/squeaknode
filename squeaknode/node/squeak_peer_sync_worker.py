import logging

from squeaknode.node.periodic_worker import PeriodicWorker
from squeaknode.node.squeak_controller import SqueakController


logger = logging.getLogger(__name__)


class SqueakPeerSyncWorker(PeriodicWorker):

    def __init__(
        self,
        squeak_controller: SqueakController,
        sync_interval_s,
    ):
        self.squeak_controller = squeak_controller
        self.sync_interval_s = sync_interval_s

    def work_fn(self):
        logger.debug("Syncing timeline with peers...")
        self.squeak_controller.sync_timeline()

    def get_interval_s(self):
        return self.sync_interval_s

    def get_name(self):
        return "peer_sync_worker"
