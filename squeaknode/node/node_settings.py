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
from typing import Optional

from squeaknode.core.update_twitter_stream_event import UpdateTwitterStreamEvent
from squeaknode.core.user_config import UserConfig
from squeaknode.node.listener_subscription_client import EventListener


logger = logging.getLogger(__name__)

NODE_SETTINGS_USERNAME = "default"


class NodeSettings:

    def __init__(self, squeak_db):
        self.squeak_db = squeak_db
        self.username = NODE_SETTINGS_USERNAME
        self.twitter_bearer_token_change_listener = EventListener()

    def insert_user_config(self) -> Optional[str]:
        user_config = UserConfig(username=self.username)
        return self.squeak_db.insert_config(user_config)

    def set_sell_price_msat(self, sell_price_msat: int) -> None:
        self.insert_user_config()
        if sell_price_msat < 0:
            raise Exception("Sell price cannot be negative.")
        self.squeak_db.set_config_sell_price_msat(
            username=self.username,
            sell_price_msat=sell_price_msat,
        )

    def clear_sell_price_msat(self) -> None:
        self.insert_user_config()
        self.squeak_db.clear_config_sell_price_msat(
            username=self.username,
        )

    def get_sell_price_msat(self) -> Optional[int]:
        user_config = self.squeak_db.get_config(
            username=self.username,
        )
        if user_config is None:
            return None
        return user_config.sell_price_msat

    def set_twitter_bearer_token(self, twitter_bearer_token: str) -> None:
        self.insert_user_config()
        self.squeak_db.set_config_twitter_bearer_token(
            username=self.username,
            twitter_bearer_token=twitter_bearer_token,
        )
        self.create_update_twitter_bearer_token_event()

    def get_twitter_bearer_token(self) -> Optional[str]:
        user_config = self.squeak_db.get_config(
            username=self.username,
        )
        if user_config is None:
            return None
        return user_config.twitter_bearer_token

    def create_update_twitter_bearer_token_event(self):
        self.twitter_bearer_token_change_listener.handle_new_item(
            UpdateTwitterStreamEvent()
        )

    def subscribe_new_bearer_token_events(self, stopped: threading.Event):
        yield from self.twitter_bearer_token_change_listener.yield_items(stopped)
