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
    stopped,
    max_queue_size=DEFAULT_MAX_QUEUE_SIZE,
    update_interval_s=DEFAULT_UPDATE_INTERVAL_S,
):
    """Custom context manager for opening a received payments client."""
    def wait_for_stop(payment_queue: queue.Queue):
        logger.info(
            "Waiting for stop event in OpenReceivedPaymentsSubscriptionClient...")
        stopped.wait()
        logger.info(
            "Cancelled subscription in OpenReceivedPaymentsSubscriptionClient.")
        # Put the poison pill
        payment_queue.put(None)

    # Create the payment queue
    q = queue.Queue(max_queue_size)

    # Start the thread to wait for stop event.
    t = threading.Thread(
        target=wait_for_stop,
        args=(q,),
    )
    t.start()

    # Create the client
    client = ReceivedPaymentsSubscriptionClient(
        squeak_db,
        initial_index,
        q,
        update_interval_s,
    )

    # Start the client
    client.start()
    try:
        yield client
    finally:
        # Stop the client
        client.stop()


class ReceivedPaymentsSubscriptionClient:
    def __init__(
        self,
        squeak_db,
        initial_index,
        payment_queue,
        update_interval_s,
    ):
        self.squeak_db = squeak_db
        self.initial_index = initial_index
        self.update_interval_s = update_interval_s
        self._queue = payment_queue
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
            try:
                for payment in self._get_received_payments_from_db(payment_index):
                    self._queue.put(payment)
                    payment_index = payment.received_payment_id
                    logger.info(
                        "Added payment to queue. Size: {}".format(
                            self._queue.qsize())
                    )
            except Exception:
                logger.error(
                    "Exception while populating queue.",
                    exc_info=True,
                )
            time.sleep(self.update_interval_s)

    def _get_received_payments_from_db(self, payment_index):
        return self.squeak_db.yield_received_payments_from_index(payment_index)

    def get_received_payments(self):
        while True:
            payment = self._queue.get()
            if payment is None:
                raise Exception("Poison pill swallowed.")
            yield payment
            self._queue.task_done()
            logger.info(
                "Removed payment from queue. Size: {}".format(
                    self._queue.qsize())
            )
