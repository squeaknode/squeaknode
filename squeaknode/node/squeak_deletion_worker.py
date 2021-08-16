import logging

from squeaknode.node.periodic_worker import PeriodicWorker
from squeaknode.node.squeak_controller import SqueakController

logger = logging.getLogger(__name__)


class SqueakDeletionWorker(PeriodicWorker):
    def __init__(
        self,
        squeak_controller: SqueakController,
        clean_interval_s: int,
    ):
        self.squeak_controller = squeak_controller
        self.clean_interval_s = clean_interval_s

    def work_fn(self):
        logger.info("Deleting old squeaks...")
        self.squeak_controller.delete_old_squeaks()

    def get_interval_s(self):
        return self.clean_interval_s

    def get_name(self):
        return "squeak_deletion_worker"
