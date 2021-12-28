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
from squeak.messages import msg_getdata
from squeak.messages import MSG_SECRET_KEY
from squeak.messages import MSG_SQUEAK
from squeak.messages import MsgSerializable
from squeak.net import CInterested
from squeak.net import CInv
from squeak.net import CSqueakLocator

from squeaknode.core.block_range import BlockRange
from squeaknode.core.interests import squeak_matches_interest
from squeaknode.core.lightning_address import LightningAddressHostPort
from squeaknode.core.offer import Offer
from squeaknode.core.peer_address import PeerAddress
from squeaknode.core.sent_offer import SentOffer
from squeaknode.core.squeak_core import SqueakCore
from squeaknode.node.active_download_manager import ActiveDownload
from squeaknode.node.downloaded_object import DownloadedOffer
from squeaknode.node.downloaded_object import DownloadedSqueak
from squeaknode.node.price_policy import PricePolicy
from squeaknode.node.secret_key_reply import FreeSecretKeyReply
from squeaknode.node.secret_key_reply import OfferReply
from squeaknode.node.secret_key_reply import SecretKeyReply
from squeaknode.node.squeak_store import SqueakStore


logger = logging.getLogger(__name__)


EMPTY_HASH = b'\x00' * 32


class NetworkHandler:

    def __init__(
        self,
        squeak_store: SqueakStore,
        squeak_core: SqueakCore,
        network_manager,
        download_manager,
        node_settings,
        config,
    ):
        self.squeak_store = squeak_store
        self.squeak_core = squeak_core
        self.network_manager = network_manager
        self.active_download_manager = download_manager
        self.node_settings = node_settings
        self.config = config

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
        self.squeak_store.save_secret_key(
            squeak_hash,
            secret_key,
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
        if price_msat == 0:
            return self.get_free_squeak_secret_key_reply(
                squeak_hash,
            )
        else:
            return self.get_offer_reply(
                squeak_hash,
                lnd_external_address,
                peer_address,
                price_msat,
            )

    def get_offer_reply(
            self,
            squeak_hash: bytes,
            lnd_external_address: Optional[LightningAddressHostPort],
            peer_address: PeerAddress,
            price_msat: int,
    ) -> Optional[OfferReply]:
        sent_offer = self.get_sent_offer_for_peer(
            squeak_hash,
            peer_address,
            price_msat,
        )
        if sent_offer is None:
            return None
        try:
            offer = self.squeak_core.package_offer(
                sent_offer,
                lnd_external_address,
            )
            return OfferReply(
                squeak_hash=squeak_hash,
                offer=offer,
            )
        except Exception:
            return None

    def get_free_squeak_secret_key_reply(self, squeak_hash: bytes) -> Optional[FreeSecretKeyReply]:
        secret_key = self.squeak_store.get_squeak_secret_key(squeak_hash)
        if secret_key is None:
            return None
        return FreeSecretKeyReply(
            squeak_hash=squeak_hash,
            secret_key=secret_key,
        )

    def get_sent_offer_for_peer(
            self,
            squeak_hash: bytes,
            peer_address: PeerAddress,
            price_msat: int,
    ) -> Optional[SentOffer]:
        # Check if there is an existing offer for the hash/peer_address combination
        sent_offer = self.squeak_store.get_sent_offer_by_squeak_hash_and_peer(
            squeak_hash,
            peer_address,
        )
        if sent_offer:
            return sent_offer
        squeak = self.squeak_store.get_squeak(squeak_hash)
        secret_key = self.squeak_store.get_squeak_secret_key(squeak_hash)
        if squeak is None or secret_key is None:
            return None
        try:
            sent_offer = self.squeak_core.create_offer(
                squeak,
                secret_key,
                peer_address,
                price_msat,
            )
        except Exception:
            logger.exception("Failed to create offer.")
            return None
        self.squeak_store.save_sent_offer(sent_offer)
        return sent_offer

    def save_received_offer(self, offer: Offer, peer_address: PeerAddress) -> Optional[int]:
        squeak = self.squeak_store.get_squeak(offer.squeak_hash)
        secret_key = self.squeak_store.get_squeak_secret_key(offer.squeak_hash)
        if squeak is None or secret_key is not None:
            return None
        try:
            # TODO: Call unpack_offer with check_payment_point=True.
            received_offer = self.squeak_core.unpack_offer(
                squeak,
                offer,
                peer_address,
            )
        except Exception:
            logger.exception("Failed to save received offer.")
            return None
        return self.squeak_store.save_received_offer(received_offer)

    def get_reply_invs(self, interest):
        squeak_hashes = self.get_local_squeaks(interest)
        secret_key_hashes = self.get_local_secret_keys(interest)
        squeak_invs = [
            CInv(type=MSG_SQUEAK, hash=squeak_hash)
            for squeak_hash in squeak_hashes]
        secret_key_invs = [
            CInv(type=MSG_SECRET_KEY, hash=squeak_hash)
            for squeak_hash in secret_key_hashes]
        return squeak_invs + secret_key_invs

    def get_local_squeaks(self, interest: CInterested):
        min_block = interest.nMinBlockHeight if interest.nMinBlockHeight != -1 else None
        max_block = interest.nMaxBlockHeight if interest.nMaxBlockHeight != -1 else None
        reply_to_hash = interest.hashReplySqk if interest.hashReplySqk != EMPTY_HASH else None
        return self.squeak_store.lookup_squeaks(
            interest.pubkeys,
            min_block,
            max_block,
            reply_to_hash,
        )

    def get_local_secret_keys(self, interest: CInterested):
        min_block = interest.nMinBlockHeight if interest.nMinBlockHeight != -1 else None
        max_block = interest.nMaxBlockHeight if interest.nMaxBlockHeight != -1 else None
        reply_to_hash = interest.hashReplySqk if interest.hashReplySqk != EMPTY_HASH else None
        return self.squeak_store.lookup_secret_keys(
            interest.pubkeys,
            min_block,
            max_block,
            reply_to_hash,
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

    def handle_received_offer(self, offer: Offer, peer_address: PeerAddress) -> Optional[int]:
        received_offer_id = self.save_received_offer(
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

    def get_interested_locator(self) -> CSqueakLocator:
        block_range = self.get_interested_block_range()
        followed_public_keys = self.squeak_store.get_followed_public_keys()
        if len(followed_public_keys) == 0:
            return CSqueakLocator(
                vInterested=[],
            )
        interests = [
            CInterested(
                pubkeys=followed_public_keys,
                nMinBlockHeight=block_range.min_block,
                nMaxBlockHeight=block_range.max_block,
            )
        ]
        return CSqueakLocator(
            vInterested=interests,
        )

    def get_interested_block_range(self) -> BlockRange:
        max_block = self.squeak_core.get_best_block_height()
        min_block = max(
            0,
            # TODO: rename this.
            max_block - self.config.node.interest_block_interval,
        )
        return BlockRange(min_block, max_block)
