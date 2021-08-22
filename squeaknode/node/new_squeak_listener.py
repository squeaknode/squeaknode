import logging
import queue
import threading
import uuid
from contextlib import contextmanager

logger = logging.getLogger(__name__)

DEFAULT_MAX_QUEUE_SIZE = 1000
DEFAULT_UPDATE_INTERVAL_S = 1


class NewSqueakListener:

    def __init__(self):
        self.callbacks = {}

    def handle_new_squeak(self, squeak):
        # logger.info("Handling new squeak: {!r}".format(
        #     get_hash(squeak).hex(),
        # ))
        for callback in self.callbacks.values():
            callback(squeak)

    def add_callback(self, name, callback):
        self.callbacks[name] = callback

    def remove_callback(self, name):
        del self.callbacks[name]


class NewSqueakSubscriptionClient:

    def __init__(
        self,
        new_squeak_listener: NewSqueakListener,
        stopped: threading.Event,
        max_queue_size=DEFAULT_MAX_QUEUE_SIZE,
    ):
        self.new_squeak_listener = new_squeak_listener
        self.stopped = stopped
        self.q: queue.Queue = queue.Queue(max_queue_size)

    @contextmanager
    def open_subscription(self):
        threading.Thread(
            target=self.wait_for_stopped,
        ).start()
        # Register the callback to populate the queue
        callback_name = "new_squeak_callback_{}".format(uuid.uuid1()),
        try:
            self.new_squeak_listener.add_callback(
                name=callback_name,
                callback=self.enqueue_squeak,
            )
            logger.info("Before yielding new squeaks client...")
            yield self
            logger.info("After yielding new squeaks client...")
        finally:
            logger.info("Stopping new squeaks client...")
            self.new_squeak_listener.remove_callback(
                name=callback_name,
            )
            logger.info("Stopped new squeaks client...")

    def enqueue_squeak(self, squeak):
        self.q.put(squeak)

    def wait_for_stopped(self):
        self.stopped.wait()
        self.q.put(None)

    def get_squeak(self):
        while True:
            item = self.q.get()
            if item is None:
                logger.debug("Poison pill swallowed.")
                return
            yield item
            self.q.task_done()
            logger.info(
                "Removed item from queue. Size: {}".format(
                    self.q.qsize())
            )
