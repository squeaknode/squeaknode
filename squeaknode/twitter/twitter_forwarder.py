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

from squeaknode.core.twitter_account_entry import TwitterAccountEntry
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

    def is_processing(self) -> bool:
        with self.lock:
            if self.current_task is not None:
                return self.current_task.is_processing()
            return False


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
        self.lock = threading.Lock()

    def start_processing(self):
        logger.info("Starting twitter forwarder task.")
        threading.Thread(
            target=self.process_forward_tweets,
            daemon=True,
        ).start()

    def setup_stream(self, bearer_token, handles):
        logger.info("Starting Twitter stream with bearer token: {} and twitter handles: {}".format(
            bearer_token,
            handles,
        ))
        with self.lock:
            if self.stopped.is_set():
                return
            twitter_stream = TwitterStream(bearer_token, handles)
            self.tweet_stream = twitter_stream.get_tweets()

    def stop_processing(self):
        logger.info("Stopping twitter forwarder task.")
        with self.lock:
            self.stopped.set()
            if self.tweet_stream is not None:
                self.tweet_stream.cancel_fn()

    def is_processing(self) -> bool:
        return self.tweet_stream is not None

    def process_forward_tweets(self):
        # Do exponential backoff
        wait_s = self.retry_s

        while not self.stopped.is_set():
            try:
                bearer_token = self.get_bearer_token()
                handles = self.get_twitter_handles()
                if not bearer_token:
                    return
                if not handles:
                    return
                self.setup_stream(bearer_token, handles)
                for tweet in self.tweet_stream.result_stream:
                    self.handle_tweet(tweet)
            # TODO: use more specific error.
            except Exception:
                self.tweet_stream = None
                logger.exception(
                    "Unable to subscribe tweet stream. Retrying in {} seconds...".format(
                        wait_s,
                    ),
                )
                self.stopped.wait(wait_s)
                wait_s *= 2

    def get_bearer_token(self) -> str:
        return self.squeak_controller.get_twitter_bearer_token() or ''

    def get_twitter_handles(self) -> List[str]:
        twitter_accounts = self.squeak_controller.get_twitter_accounts()
        handles = [account.handle for account in twitter_accounts]
        return handles

    def is_tweet_a_match(self, tweet: dict, account: TwitterAccountEntry) -> bool:
        for rule in tweet['matching_rules']:
            if rule['tag'] == account.handle:
                return True
        return False

    def forward_tweet(self, tweet: dict, account: TwitterAccountEntry) -> None:
        self.squeak_controller.make_squeak(
            profile_id=account.profile_id,
            content_str=tweet['data']['text'],
            replyto_hash=None,
        )

    def handle_tweet(self, tweet: dict):
        logger.info(
            "Got tweet: {}".format(tweet))
        twitter_accounts = self.squeak_controller.get_twitter_accounts()
        for account in twitter_accounts:
            if self.is_tweet_a_match(tweet, account):
                self.forward_tweet(tweet, account)
