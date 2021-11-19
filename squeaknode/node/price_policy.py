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
from typing import Optional

from squeak.core import CSqueak

from squeaknode.config.config import SqueaknodeConfig
from squeaknode.core.peer_address import PeerAddress
from squeaknode.core.squeak_peer import SqueakPeer
from squeaknode.core.user_config import UserConfig
from squeaknode.db.squeak_db import SqueakDb


logger = logging.getLogger(__name__)


class PricePolicy:

    def __init__(self, squeak_db: SqueakDb, config: SqueaknodeConfig):
        self.squeak_db = squeak_db
        self.config = config

    def get_price(self, squeak: CSqueak, peer_address: PeerAddress) -> int:
        """Get the price to sell this squeak to this peer.

        """
        # Return zero for price if peer is configured to be share for free.
        peer = self.get_peer(peer_address)
        if peer is not None and peer.share_for_free:
            return 0
        # Return sell price from settings if configured
        sell_price = self.get_sell_price_msat()
        if sell_price is not None:
            return sell_price
        return self.get_default_price()

    def get_peer(self, peer_address: PeerAddress) -> Optional[SqueakPeer]:
        return self.squeak_db.get_peer_by_address(peer_address)

    def get_default_price(self) -> int:
        return self.config.node.price_msat

    def get_user_config(self) -> Optional[UserConfig]:
        return self.squeak_db.get_config(
            username=self.config.webadmin.username,
        )

    def get_sell_price_msat(self) -> Optional[int]:
        user_config = self.get_user_config()
        if user_config is None:
            return None
        return user_config.sell_price_msat
