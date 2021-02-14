import logging
import queue
import threading
from contextlib import contextmanager

logger = logging.getLogger(__name__)

DEFAULT_MAX_QUEUE_SIZE = 1000
DEFAULT_UPDATE_INTERVAL_S = 1


class ReceivedPaymentsSubscriptionClient:
    def __init__(
        self,
        squeak_db,
        initial_index: int,
        stopped: threading.Event,
        max_queue_size=DEFAULT_MAX_QUEUE_SIZE,
        update_interval_s=DEFAULT_UPDATE_INTERVAL_S,
    ):
        self.squeak_db = squeak_db
        self.initial_index = initial_index
        self.stopped = stopped
        self.update_interval_s = update_interval_s
        self.q: queue.Queue = queue.Queue(max_queue_size)

    @contextmanager
    def open_subscription(self):
        # Start the thread to populate the queue.
        threading.Thread(
            target=self.populate_queue,
        ).start()
        try:
            logger.info("Before yielding received payment client...")
            yield self
            logger.info("After yielding received payment client...")
        finally:
            logger.info("Stopping received payment client...")
            self.stopped.set()
            logger.info("Stopped received payment client...")

    def populate_queue(self):
        payment_index = self.initial_index
        while not self.stopped.is_set():
            try:
                for payment in self.get_latest_received_payments(payment_index):
                    self.q.put(payment)
                    payment_index = payment.received_payment_id
                    logger.info(
                        "Added payment to queue. Size: {}".format(
                            self.q.qsize())
                    )
            except Exception:
                logger.error(
                    "Exception while populating queue.",
                    exc_info=True,
                )
            self.stopped.wait(self.update_interval_s)
        # Put the poison pill
        logger.info("Putting poison pill in queue...")
        self.q.put(None)

    def get_latest_received_payments(self, payment_index):
        return self.squeak_db.yield_received_payments_from_index(
            payment_index,
        )

    def get_received_payments(self):
        while True:
            payment = self.q.get()
            if payment is None:
                raise Exception("Poison pill swallowed.")
            yield payment
            self.q.task_done()
            logger.info(
                "Removed payment from queue. Size: {}".format(
                    self.q.qsize())
            )
