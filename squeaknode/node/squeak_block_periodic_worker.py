import logging
import threading

logger = logging.getLogger(__name__)


VERIFY_UPDATE_INTERVAL_S = 60.0


class SqueakBlockPeriodicWorker:
    def __init__(self, squeak_controller):
        self.squeak_controller = squeak_controller

    def start_running(self):
        threading.Timer(VERIFY_UPDATE_INTERVAL_S, self.start_running).start()
        self.squeak_controller.verify_all_unverified_squeaks()
