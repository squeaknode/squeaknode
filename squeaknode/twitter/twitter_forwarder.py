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
from typing import List
from typing import Optional

from squeaknode.node.squeak_controller import SqueakController
from squeaknode.twitter.twitter_stream import TwitterStream


logger = logging.getLogger(__name__)


class TwitterForwarder:

    def __init__(
            self,
            retry_s: int,
    ):
        self.retry_s = retry_s
        self.lock = threading.Lock()
        self.current_task: Optional[TwitterForwarderTask] = None

    def start_processing(self, squeak_controller: SqueakController):
        with self.lock:
            if self.current_task is not None:
                self.current_task.stop_processing()
            self.current_task = TwitterForwarderTask(
                squeak_controller,
                self.retry_s,
            )
            self.current_task.start_processing()

    def stop_processing(self):
        with self.lock:
            if self.current_task is not None:
                self.current_task.stop_processing()


class TwitterForwarderTask:

    def __init__(
        self,
        squeak_controller: SqueakController,
        retry_s: int,
    ):
        self.squeak_controller = squeak_controller
        self.retry_s = retry_s
        self.stopped = threading.Event()
        self.tweet_stream = None

    def start_processing(self):
        logger.info("Starting twitter forwarder task.")
        threading.Thread(
            target=self.process_forward_tweets,
            daemon=True,
        ).start()

    def stop_processing(self):
        logger.info("Stopping twitter forwarder task.")
        self.stopped.set()

    def process_forward_tweets(self):
        while not self.stopped.is_set():
            try:
                bearer_token = self.get_bearer_token()
                handles = self.get_twitter_handles()
                logger.info("Starting forward tweets with bearer token: {} and twitter handles: {}".format(
                    bearer_token,
                    handles,
                ))
                twitter_stream = TwitterStream(bearer_token, handles)
                self.tweet_stream = twitter_stream.get_tweets()
                if self.stopped.is_set():
                    return
                for tweet in self.tweet_stream:
                    self.handle_tweet(tweet)
            # TODO: use more specific error.
            except Exception:
                logger.exception(
                    "Unable to subscribe tweet stream. Retrying in {} seconds...".format(
                        self.retry_s,
                    ),
                )
                self.stopped.wait(self.retry_s)

    def get_bearer_token(self) -> str:
        # TODO.
        # return 'abcdefg'
        return self.squeak_controller.get_twitter_bearer_token() or ''

    def get_twitter_handles(self) -> List[str]:
        # TODO.
        return ['alice', 'bob', 'rterqwerqeqwe']

    def handle_tweet(self, tweet: dict):
        logger.info(
            "Got tweet: {}".format(tweet))
        # received_payment_id = self.squeak_db.insert_received_payment(
        #     received_payment,
        # )
        # if received_payment_id is not None:
        #     logger.debug(
        #         "Saved received payment: {}".format(received_payment))
