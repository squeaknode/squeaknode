# MIT License
#
# Copyright (c) 2020 Jonathan Zernik
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.
import logging
import queue
import threading
import uuid
from contextlib import contextmanager

from squeaknode.network.connection_manager import ConnectionManager


logger = logging.getLogger(__name__)

DEFAULT_MAX_QUEUE_SIZE = 1000
DEFAULT_UPDATE_INTERVAL_S = 1


class ConnectedPeersSubscriptionClient:
    def __init__(
        self,
        connection_manager: ConnectionManager,
        stopped: threading.Event,
        max_queue_size=DEFAULT_MAX_QUEUE_SIZE,
    ):
        self.connection_manager = connection_manager
        self.stopped = stopped
        self.q: queue.Queue = queue.Queue(max_queue_size)

    @contextmanager
    def open_subscription(self):
        threading.Thread(
            target=self.wait_for_stopped,
        ).start()
        # Register the callback to populate the queue
        callback_name = "peers_changed_callback_{}".format(uuid.uuid1()),
        try:
            self.connection_manager.add_peers_changed_callback(
                name=callback_name,
                callback=self.enqueue_connected_peers,
            )
            logger.debug("Before yielding connected peers client...")
            yield self
            logger.debug("After yielding connected peers client...")
        finally:
            logger.debug("Stopping connected peers client...")
            self.connection_manager.remove_peers_changed_callback(
                name=callback_name,
            )
            logger.debug("Stopped connected peers client...")

    def enqueue_connected_peers(self, connected_peers):
        self.q.put(connected_peers)

    def wait_for_stopped(self):
        self.stopped.wait()
        self.q.put(None)

    def get_connected_peers(self):
        while True:
            item = self.q.get()
            if item is None:
                logger.debug("Poison pill swallowed.")
                return
            yield item
            self.q.task_done()
            logger.debug(
                "Removed item from queue. Size: {}".format(
                    self.q.qsize())
            )
