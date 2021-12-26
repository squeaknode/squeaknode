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

from squeak.core import CSqueak
from squeak.core.keys import SqueakPublicKey
from squeak.messages import msg_getdata
from squeak.messages import MSG_SECRET_KEY
from squeak.messages import MSG_SQUEAK
from squeak.messages import MsgSerializable
from squeak.net import CInterested
from squeak.net import CInv
from squeak.net import CSqueakLocator

from squeaknode.core.interests import squeak_matches_interest
from squeaknode.core.lightning_address import LightningAddressHostPort
from squeaknode.core.offer import Offer
from squeaknode.core.peer_address import PeerAddress
from squeaknode.node.active_download_manager import ActiveDownload
from squeaknode.node.downloaded_object import DownloadedOffer
from squeaknode.node.downloaded_object import DownloadedSqueak
from squeaknode.node.price_policy import PricePolicy
from squeaknode.node.secret_key_reply import SecretKeyReply
from squeaknode.node.squeak_store import SqueakStore

logger = logging.getLogger(__name__)


EMPTY_HASH = b'\x00' * 32


class NetworkHandler:

    def __init__(
        self,
        squeak_store: SqueakStore,
        network_manager,
        download_manager,
        node_settings,
        config,
    ):
        self.squeak_store = squeak_store
        self.network_manager = network_manager
        self.active_download_manager = download_manager
        self.node_settings = node_settings
        self.config = config

    def get_interested_locator(self) -> CSqueakLocator:
        return self.squeak_store.get_interested_locator()

    def get_squeak(self, squeak_hash: bytes) -> Optional[CSqueak]:
        return self.squeak_store.get_squeak(squeak_hash)

    def get_squeak_secret_key(self, squeak_hash: bytes) -> Optional[bytes]:
        return self.squeak_store.get_squeak_secret_key(squeak_hash)

    def get_unknown_invs(self, invs):
        unknown_squeak_invs = self.get_unknown_squeaks(invs)
        unknown_secret_key_invs = self.get_unknown_secret_keys(invs)
        return unknown_squeak_invs + unknown_secret_key_invs

    def get_unknown_squeaks(self, invs):
        return [
            inv for inv in invs
            if inv.type == MSG_SQUEAK
            and self.get_squeak(inv.hash) is None
        ]

    def get_unknown_secret_keys(self, invs):
        return [
            inv for inv in invs
            if inv.type == MSG_SECRET_KEY
            and self.get_squeak(inv.hash) is not None
            and self.get_squeak_secret_key(inv.hash) is None
        ]

    def save_squeak(self, squeak: CSqueak) -> Optional[bytes]:
        # return self.squeak_store.save_squeak(squeak)
        return self.save_active_download_squeak(squeak) or \
            self.save_followed_squeak(squeak)

    def save_active_download_squeak(self, squeak: CSqueak) -> Optional[bytes]:
        """Save the given squeak as an active download.

        Returns:
          bytes: the hash of the saved squeak.
        """
        counter = self.get_download_squeak_counter(squeak)
        if counter is None:
            return None
        saved_squeak_hash = self.squeak_store.save_squeak(squeak)
        if saved_squeak_hash is None:
            return None
        counter.increment()
        return saved_squeak_hash

    def save_followed_squeak(self, squeak: CSqueak) -> Optional[bytes]:
        """Save the given squeak because it matches the followed
        interest criteria.

        Returns:
          bytes: the hash of the saved squeak.
        """
        if not self.squeak_matches_interest(squeak):
            return None
        # TODO: catch exception if save_squeak fails (because of rate limit, for example).
        return self.squeak_store.save_squeak(squeak)

    def squeak_matches_interest(self, squeak: CSqueak) -> bool:
        locator = self.get_interested_locator()
        for interest in locator.vInterested:
            if squeak_matches_interest(squeak, interest):
                return True
        return False

    def unlock_squeak(self, squeak_hash: bytes, secret_key: bytes):
        return self.squeak_store.unlock_squeak(squeak_hash, secret_key)

    def get_reply_invs(self, interest):
        squeak_hashes = self._get_local_squeaks(interest)
        secret_key_hashes = self._get_local_secret_keys(interest)
        squeak_invs = [
            CInv(type=MSG_SQUEAK, hash=squeak_hash)
            for squeak_hash in squeak_hashes]
        secret_key_invs = [
            CInv(type=MSG_SECRET_KEY, hash=squeak_hash)
            for squeak_hash in secret_key_hashes]
        return squeak_invs + secret_key_invs

    def _get_local_squeaks(self, interest: CInterested):
        min_block = interest.nMinBlockHeight if interest.nMinBlockHeight != -1 else None
        max_block = interest.nMaxBlockHeight if interest.nMaxBlockHeight != -1 else None
        reply_to_hash = interest.hashReplySqk if interest.hashReplySqk != EMPTY_HASH else None
        return self.lookup_squeaks(
            public_keys=interest.pubkeys,
            min_block=min_block,
            max_block=max_block,
            reply_to_hash=reply_to_hash,
        )

    def _get_local_secret_keys(self, interest: CInterested):
        min_block = interest.nMinBlockHeight if interest.nMinBlockHeight != -1 else None
        max_block = interest.nMaxBlockHeight if interest.nMaxBlockHeight != -1 else None
        reply_to_hash = interest.hashReplySqk if interest.hashReplySqk != EMPTY_HASH else None
        return self.lookup_secret_keys(
            public_keys=interest.pubkeys,
            min_block=min_block,
            max_block=max_block,
            reply_to_hash=reply_to_hash,
        )

    def lookup_squeaks(
            self,
            public_keys: List[SqueakPublicKey],
            min_block: Optional[int],
            max_block: Optional[int],
            reply_to_hash: Optional[bytes],
    ) -> List[bytes]:
        return self.squeak_store.lookup_squeaks(
            public_keys,
            min_block,
            max_block,
            reply_to_hash,
        )

    def lookup_secret_keys(
            self,
            public_keys: List[SqueakPublicKey],
            min_block: Optional[int],
            max_block: Optional[int],
            reply_to_hash: Optional[bytes],
    ) -> List[bytes]:
        return self.squeak_store.lookup_secret_keys(
            public_keys,
            min_block,
            max_block,
            reply_to_hash,
        )

    def get_secret_key_reply(self, squeak_hash: bytes, peer_address: PeerAddress) -> Optional[SecretKeyReply]:
        squeak = self.get_squeak(squeak_hash)
        price_msat = self.get_price_for_squeak(squeak, peer_address)
        lnd_external_address: Optional[LightningAddressHostPort] = None
        if self.config.lnd.external_host:
            lnd_external_address = LightningAddressHostPort(
                host=self.config.lnd.external_host,
                port=self.config.lnd.port,
            )
        return self.squeak_store.get_secret_key_reply(
            squeak_hash,
            lnd_external_address,
            peer_address,
            price_msat,
        )

    def request_offers(self, squeak_hash: bytes):
        logger.info("Requesting offers for squeak: {}".format(
            squeak_hash.hex(),
        ))
        invs = [
            CInv(type=2, hash=squeak_hash)
        ]
        getdata_msg = msg_getdata(inv=invs)
        self.broadcast_msg(getdata_msg)

    def save_received_offer(self, offer: Offer, peer_address: PeerAddress) -> Optional[int]:
        # return self.squeak_store.save_received_offer(offer, peer_address)
        received_offer_id = self.squeak_store.save_received_offer(
            offer,
            peer_address,
        )
        if received_offer_id is None:
            return None
        counter = self.get_download_offer_counter(offer)
        if counter is not None:
            counter.increment()
        return received_offer_id

    def get_download_offer_counter(self, offer: Offer) -> Optional[ActiveDownload]:
        downloaded_offer = DownloadedOffer(offer)
        return self.active_download_manager.lookup_counter(downloaded_offer)

    def get_download_squeak_counter(self, squeak: CSqueak) -> Optional[ActiveDownload]:
        downloaded_squeak = DownloadedSqueak(squeak)
        return self.active_download_manager.lookup_counter(downloaded_squeak)

    def get_price_for_squeak(self, squeak: CSqueak, peer_address: PeerAddress) -> int:
        price_policy = PricePolicy(
            self.squeak_store,
            self.config,
            self.node_settings,
        )
        return price_policy.get_price(squeak, peer_address)

    def broadcast_msg(self, msg: MsgSerializable) -> int:
        return self.network_manager.broadcast_msg(msg)
