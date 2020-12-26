import logging
import queue
import threading
import time
from contextlib import contextmanager

logger = logging.getLogger(__name__)

DEFAULT_MAX_QUEUE_SIZE = 1000
DEFAULT_UPDATE_INTERVAL_S = 1


@contextmanager
def OpenReceivedPaymentsSubscriptionClient(
    squeak_db,
    initial_index,
    max_queue_size=DEFAULT_MAX_QUEUE_SIZE,
    update_interval_s=DEFAULT_UPDATE_INTERVAL_S,
):
    """Custom context manager for opening a received payments client."""

    # f = open(filename, method)
    client = ReceivedPaymentsSubscriptionClient(
        squeak_db,
        initial_index,
        max_queue_size,
        update_interval_s,
    )
    client.start()
    try:
        # yield f
        yield client

    finally:
        # f.close()
        client.stop()


class ReceivedPaymentsSubscriptionClient:
    def __init__(
        self,
        squeak_db,
        initial_index,
        max_queue_size=DEFAULT_MAX_QUEUE_SIZE,
        update_interval_s=DEFAULT_UPDATE_INTERVAL_S,
    ):
        self.squeak_db = squeak_db
        self.initial_index = initial_index
        self.update_interval_s = update_interval_s
        self._queue = queue.Queue(max_queue_size)
        self._stopped = threading.Event()

    @property
    def queue(self):
        return self._queue

    def start(self):
        logger.info("Starting received payments subscription client...")
        populate_queue_thread = threading.Thread(
            target=self._populate_queue,
            args=(),
        )
        populate_queue_thread.start()

    def stop(self):
        logger.info("Stopping received payments subscription client...")
        self._stopped.set()

    def _populate_queue(self):
        payment_index = self.initial_index
        while not self._stopped.is_set():
            for payment in self._get_received_payments_from_db(payment_index):
                self._queue.put(payment)
                payment_index = payment.received_payment_id
                logger.info(
                    "Added payment to queue. Size: {}".format(self._queue.qsize())
                )
            time.sleep(self.update_interval_s)

    def _get_received_payments_from_db(self, payment_index):
        return self.squeak_db.yield_received_payments_from_index(payment_index)

    def get_received_payments(self):
        while True:
            payment = self._queue.get()
            yield payment
            self._queue.task_done()
            logger.info(
                "Removed payment from queue. Size: {}".format(self._queue.qsize())
            )
