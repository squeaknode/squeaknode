import logging
import threading


logger = logging.getLogger(__name__)


class PaymentProcessor:

    def __init__(
        self,
        squeak_controller,
        retry_s: int = 10,
    ):
        self.squeak_controller = squeak_controller
        self.retry_s = retry_s
        self.stopped = threading.Event()
        self.stopped_permanently = threading.Event()
        self.lock = threading.Lock()

    def start_processing(self):
        with self.lock:
            if self.stopped_permanently.is_set():
                return
            self.stopped.set()
            self.stopped = threading.Event()
            threading.Thread(
                target=self.squeak_controller.process_subscribed_invoices,
                args=(self.stopped,),
            ).start()

    def stop_processing(self, permanent=False):
        with self.lock:
            self.stopped.set()
            if permanent:
                self.stopped_permanently.set()
