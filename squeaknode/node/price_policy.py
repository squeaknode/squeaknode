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
from squeaknode.node.node_settings import NodeSettings
from squeaknode.node.squeak_store import SqueakStore


logger = logging.getLogger(__name__)


class PricePolicy:

    def __init__(self, squeak_store: SqueakStore, config: SqueaknodeConfig, node_settings: NodeSettings):
        # self.squeak_db = squeak_db
        self.squeak_store = squeak_store
        self.config = config
        self.node_settings = node_settings

    def get_price(self, squeak: CSqueak, peer_address: PeerAddress) -> int:
        """Get the price to sell this squeak to this peer.

        """
        # Return zero for price if peer is configured to be share for free.
        peer = self.get_peer(peer_address)
        if peer is not None and peer.share_for_free:
            return 0
        sell_price_msat = self.get_sell_price_msat()
        if sell_price_msat is None:
            return self.get_default_price()
        return sell_price_msat

    def get_peer(self, peer_address: PeerAddress) -> Optional[SqueakPeer]:
        # return self.squeak_db.get_peer_by_address(peer_address)
        return self.squeak_store.get_peer_by_address(peer_address)

    def get_default_price(self) -> int:
        return self.config.node.price_msat

    def get_sell_price_msat(self) -> Optional[int]:
        return self.node_settings.get_sell_price_msat()
