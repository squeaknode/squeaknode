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
import threading

from squeaknode.core.squeaks import get_hash
from squeaknode.node.squeak_controller import SqueakController


logger = logging.getLogger(__name__)

DEFAULT_MAX_QUEUE_SIZE = 1000
DEFAULT_UPDATE_INTERVAL_S = 1

HASH_LENGTH = 32
EMPTY_HASH = b'\x00' * HASH_LENGTH


class UpdateSubscribedSqueaksWorker:

    def __init__(self, squeak_controller: SqueakController):
        self.squeak_controller = squeak_controller
        self.stopped = threading.Event()

    def start_running(self):
        threading.Thread(
            target=self.handle_new_squeaks,
            name="new_squeaks_worker_thread",
            daemon=True,
        ).start()

    def stop_running(self):
        self.stopped.set()

    def handle_new_squeaks(self):
        logger.debug("Starting UpdateSubscribedSqueaksWorker...")
        for squeak in self.squeak_controller.subscribe_new_squeaks(
                self.stopped,
        ):
            logger.debug("Handling new squeak: {!r}".format(
                get_hash(squeak).hex(),
            ))
            # self.forward_squeak(squeak)
            self.squeak_controller.forward_squeak(squeak)
