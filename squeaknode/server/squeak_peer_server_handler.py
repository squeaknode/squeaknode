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
from typing import List
from typing import Optional

from squeak.core.keys import SqueakPublicKey

from squeaknode.core.lightning_address import LightningAddressHostPort
from squeaknode.core.offer import Offer
from squeaknode.core.peer_address import Network
from squeaknode.core.peer_address import PeerAddress
from squeaknode.node.price_policy import PricePolicy
from squeaknode.node.squeak_store import SqueakStore

logger = logging.getLogger(__name__)


class PaymentRequiredError(Exception):
    pass


class NotFoundError(Exception):
    pass


class SqueakPeerServerHandler(object):
    """Handles peer server commands."""

    def __init__(
            self,
            squeak_store: SqueakStore,
            node_settings,
            config,
    ):
        self.squeak_store = squeak_store
        self.node_settings = node_settings
        self.config = config

    def handle_get_squeak_bytes(self, squeak_hash_str) -> Optional[bytes]:
        squeak_hash = bytes.fromhex(squeak_hash_str)
        logger.info("Handle get squeak for hash: {}".format(squeak_hash_str))
        squeak = self.squeak_store.get_squeak(squeak_hash)
        if not squeak:
            raise NotFoundError()
        return squeak.serialize()

    def handle_get_secret_key(self, squeak_hash_str) -> bytes:
        squeak_hash = bytes.fromhex(squeak_hash_str)
        logger.info(
            "Handle get secret key for hash: {}".format(squeak_hash_str))
        price_msat = self.get_price_for_squeak()
        if price_msat > 0:
            raise PaymentRequiredError()
        secret_key = self.squeak_store.get_squeak_secret_key(squeak_hash)
        if not secret_key:
            raise NotFoundError()
        return secret_key

    def handle_get_offer(self, squeak_hash_str, client_host) -> Offer:
        squeak_hash = bytes.fromhex(squeak_hash_str)
        logger.info("Handle get offer for hash: {}, client_host: {}".format(
            squeak_hash_str, client_host))
        client_addr = PeerAddress(
            network=Network.IPV4,
            host=client_host,
            port=0,
        )
        logger.info("client_addr: {}".format(client_addr))
        price_msat = self.get_price_for_squeak()
        if price_msat == 0:
            raise NotFoundError()
        # TODO: lnd_external_address should be configured inside SqueakStore.
        lnd_external_address: Optional[LightningAddressHostPort] = None
        if self.config.lnd.external_host:
            lnd_external_address = LightningAddressHostPort(
                host=self.config.lnd.external_host,
                port=self.config.lnd.port,
            )
        logger.info(lnd_external_address)
        offer = self.squeak_store.get_packaged_offer(
            squeak_hash,
            client_addr,
            price_msat,
            lnd_external_address,
        )
        if not offer:
            raise NotFoundError()
        return offer

    def handle_lookup_squeaks(
            self,
            pubkey_strs: List[str],
            min_block: Optional[int],
            max_block: Optional[int],
    ) -> List[bytes]:
        pubkeys = [
            SqueakPublicKey.from_bytes(bytes.fromhex(pubkey_str))
            for pubkey_str in pubkey_strs
        ]

        # Add separate endpoint for replies.
        # reply_to_hash = interest.hashReplySqk if interest.hashReplySqk != EMPTY_HASH else None
        return self.squeak_store.lookup_squeaks(
            pubkeys,
            min_block,
            max_block,
            None,
        )

    def get_price_for_squeak(self) -> int:
        price_policy = PricePolicy(
            self.squeak_store,
            self.config,
            self.node_settings,
        )
        return price_policy.get_price()
