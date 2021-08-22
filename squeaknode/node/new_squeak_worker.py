import logging
import threading

from squeaknode.core.util import get_hash
from squeaknode.network.network_manager import NetworkManager
from squeaknode.node.squeak_controller import SqueakController


logger = logging.getLogger(__name__)

DEFAULT_MAX_QUEUE_SIZE = 1000
DEFAULT_UPDATE_INTERVAL_S = 1


class NewSqueakWorker:

    def __init__(self,
                 squeak_controller: SqueakController,
                 network_manager: NetworkManager,
                 ):
        self.squeak_controller = squeak_controller
        self.network_manager = network_manager
        self.stopped = threading.Event()

    def start_running(self):
        threading.Thread(
            target=self.handle_new_squeaks,
            name="new_squeaks_worker_thread",
        ).start()

    def stop_running(self):
        self.stopped.set()

    def handle_new_squeaks(self):
        logger.info("Starting NewSqueakWorker...")
        for squeak in self.squeak_controller.subscribe_new_squeaks(
                self.stopped,
        ):
            logger.info("Handling new squeak: {!r}".format(
                get_hash(squeak).hex(),
            ))
