import logging

from squeaknode.node.periodic_worker import PeriodicWorker
from squeaknode.node.squeak_controller import SqueakController


logger = logging.getLogger(__name__)


class PeerConnectionWorker(PeriodicWorker):
    def __init__(
        self,
        squeak_controller: SqueakController,
        connect_interval_s: int,
    ):
        self.squeak_controller = squeak_controller
        self.connect_interval_s = connect_interval_s

    def work_fn(self):
        logger.info("Connecting peers...")
        self.squeak_controller.connect_peers()

    def get_interval_s(self):
        return self.connect_interval_s

    def get_name(self):
        return "peer_connection_worker"
