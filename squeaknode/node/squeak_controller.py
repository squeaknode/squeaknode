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
from typing import Iterable
from typing import List
from typing import Optional

import squeak.params
from squeak.core import CSqueak
from squeak.core.keys import SqueakPrivateKey
from squeak.core.keys import SqueakPublicKey
from squeak.messages import msg_getdata
from squeak.messages import MsgSerializable
from squeak.net import CInterested
from squeak.net import CInv

from squeaknode.core.connected_peer import ConnectedPeer
from squeaknode.core.download_result import DownloadResult
from squeaknode.core.peer_address import PeerAddress
from squeaknode.core.received_offer import ReceivedOffer
from squeaknode.core.received_payment import ReceivedPayment
from squeaknode.core.received_payment_summary import ReceivedPaymentSummary
from squeaknode.core.sent_payment import SentPayment
from squeaknode.core.sent_payment_summary import SentPaymentSummary
from squeaknode.core.squeak_core import SqueakCore
from squeaknode.core.squeak_entry import SqueakEntry
from squeaknode.core.squeak_peer import SqueakPeer
from squeaknode.core.squeak_profile import SqueakProfile
from squeaknode.core.squeaks import get_hash
from squeaknode.core.twitter_account_entry import TwitterAccountEntry
from squeaknode.node.received_payments_subscription_client import ReceivedPaymentsSubscriptionClient
from squeaknode.node.squeak_store import SqueakStore


logger = logging.getLogger(__name__)


class SqueakController:
    """Control plane for all actions on a node.

    """

    def __init__(
        self,
        squeak_store: SqueakStore,
        squeak_core: SqueakCore,
        payment_processor,
        network_manager,
        download_manager,
        tweet_forwarder,
        node_settings,
        config,
    ):
        self.squeak_store = squeak_store
        self.squeak_core = squeak_core
        self.payment_processor = payment_processor
        self.network_manager = network_manager
        self.active_download_manager = download_manager
        self.tweet_forwarder = tweet_forwarder
        self.node_settings = node_settings
        self.config = config

    def make_squeak(
            self,
            profile_id: int,
            content_str: str,
            replyto_hash: Optional[bytes],
            recipient_profile_id: Optional[int],
    ) -> Optional[bytes]:
        squeak_profile = self.squeak_store.get_squeak_profile(profile_id)
        if squeak_profile is None:
            raise Exception("Profile with id {} not found.".format(
                profile_id,
            ))
        if recipient_profile_id:
            recipient_profile = self.squeak_store.get_squeak_profile(
                recipient_profile_id)
            if recipient_profile is None:
                raise Exception("Recipient profile with id {} not found.".format(
                    recipient_profile_id,
                ))
        squeak, secret_key = self.squeak_core.make_squeak(
            squeak_profile,
            content_str,
            replyto_hash,
            recipient_profile=recipient_profile if recipient_profile_id else None,
        )
        inserted_squeak_hash = self.squeak_store.save_squeak(squeak)
        if inserted_squeak_hash is None:
            raise Exception("Failed to save squeak.")
        self.squeak_store.save_secret_key(inserted_squeak_hash, secret_key)
        if squeak.is_private_message:
            self.squeak_store.unlock_squeak(
                inserted_squeak_hash,
                author_profile_id=profile_id,
            )
        return inserted_squeak_hash

    def pay_offer(self, received_offer_id: int) -> int:
        received_offer = self.squeak_store.get_received_offer(
            received_offer_id,
        )
        if received_offer is None:
            raise Exception("Received offer with id {} not found.".format(
                received_offer_id,
            ))
        logger.info("Paying received offer: {}".format(received_offer))
        sent_payment = self.squeak_core.pay_offer(received_offer)
        sent_payment_id = self.squeak_store.save_sent_payment(sent_payment)
        self.squeak_store.mark_received_offer_paid(
            sent_payment.payment_hash,
        )
        self.squeak_store.save_secret_key(
            received_offer.squeak_hash,
            sent_payment.secret_key,
        )
        return sent_payment_id

    def decrypt_private_squeak(
            self,
            squeak_hash: bytes,
            author_profile_id: Optional[int],
            recipient_profile_id: Optional[int],
    ):
        self.squeak_store.unlock_squeak(
            squeak_hash,
            author_profile_id=author_profile_id,
            recipient_profile_id=recipient_profile_id,
        )

    def get_squeak(self, squeak_hash: bytes) -> Optional[CSqueak]:
        return self.squeak_store.get_squeak(squeak_hash)

    # def get_squeak_secret_key(self, squeak_hash: bytes) -> Optional[bytes]:
    #     return self.squeak_store.get_squeak_secret_key(squeak_hash)

    def delete_squeak(self, squeak_hash: bytes) -> None:
        self.squeak_store.delete_squeak(squeak_hash)

    def create_signing_profile(self, profile_name: str) -> int:
        return self.squeak_store.create_signing_profile(profile_name)

    def import_signing_profile(self, profile_name: str, private_key: SqueakPrivateKey) -> int:
        return self.squeak_store.import_signing_profile(profile_name, private_key)

    def create_contact_profile(self, profile_name: str, public_key: SqueakPublicKey) -> int:
        return self.squeak_store.create_contact_profile(profile_name, public_key)

    def get_profiles(self) -> List[SqueakProfile]:
        return self.squeak_store.get_profiles()

    def get_signing_profiles(self) -> List[SqueakProfile]:
        return self.squeak_store.get_signing_profiles()

    def get_contact_profiles(self) -> List[SqueakProfile]:
        return self.squeak_store.get_contact_profiles()

    def get_squeak_profile(self, profile_id: int) -> Optional[SqueakProfile]:
        return self.squeak_store.get_squeak_profile(profile_id)

    def get_squeak_profile_by_public_key(self, public_key: SqueakPublicKey) -> Optional[SqueakProfile]:
        return self.squeak_store.get_squeak_profile_by_public_key(public_key)

    def get_squeak_profile_by_name(self, name: str) -> Optional[SqueakProfile]:
        return self.squeak_store.get_squeak_profile_by_name(name)

    def set_squeak_profile_following(self, profile_id: int, following: bool) -> None:
        return self.squeak_store.set_squeak_profile_following(profile_id, following)

    def rename_squeak_profile(self, profile_id: int, profile_name: str) -> None:
        return self.squeak_store.rename_squeak_profile(profile_id, profile_name)

    def delete_squeak_profile(self, profile_id: int) -> None:
        return self.squeak_store.delete_squeak_profile(profile_id)

    def set_squeak_profile_image(self, profile_id: int, profile_image: bytes) -> None:
        return self.squeak_store.set_squeak_profile_image(profile_id, profile_image)

    def clear_squeak_profile_image(self, profile_id: int) -> None:
        return self.squeak_store.clear_squeak_profile_image(profile_id)

    def get_squeak_profile_private_key(self, profile_id: int) -> bytes:
        return self.squeak_store.get_squeak_profile_private_key(profile_id)

    def create_peer(self, peer_name: str, peer_address: PeerAddress):
        return self.squeak_store.create_peer(peer_name, peer_address)

    def get_peer(self, peer_id: int) -> Optional[SqueakPeer]:
        return self.squeak_store.get_peer(peer_id)

    def get_peer_by_address(self, peer_address: PeerAddress) -> Optional[SqueakPeer]:
        return self.squeak_store.get_peer_by_address(peer_address)

    def get_peers(self):
        return self.squeak_store.get_peers()

    def get_autoconnect_peers(self) -> List[SqueakPeer]:
        return self.squeak_store.get_autoconnect_peers()

    def set_peer_autoconnect(self, peer_id: int, autoconnect: bool):
        return self.squeak_store.set_peer_autoconnect(peer_id, autoconnect)

    def set_peer_share_for_free(self, peer_id: int, share_for_free: bool):
        return self.squeak_store.set_peer_share_for_free(peer_id, share_for_free)

    def rename_peer(self, peer_id: int, peer_name: str):
        return self.squeak_store.rename_peer(peer_id, peer_name)

    def delete_peer(self, peer_id: int):
        return self.squeak_store.delete_peer(peer_id)

    def get_received_offers(self, squeak_hash: bytes) -> List[ReceivedOffer]:
        return self.squeak_store.get_received_offers(squeak_hash)

    def get_received_offer(self, received_offer_id: int) -> Optional[ReceivedOffer]:
        return self.squeak_store.get_received_offer(received_offer_id)

    def get_sent_payments(
            self,
            limit: int,
            last_sent_payment: Optional[SentPayment],
    ) -> List[SentPayment]:
        return self.squeak_store.get_sent_payments(
            limit,
            last_sent_payment,
        )

    def get_sent_payment(self, sent_payment_id: int) -> Optional[SentPayment]:
        return self.squeak_store.get_sent_payment(sent_payment_id)

    def get_sent_offers(self):
        return self.squeak_store.get_sent_offers()

    def get_received_payments(
            self,
            limit: int,
            last_received_payment: Optional[ReceivedPayment],
    ) -> List[ReceivedPayment]:
        return self.squeak_store.get_received_payments(
            limit,
            last_received_payment,
        )

    def delete_all_expired_offers(self):
        self.squeak_store.delete_all_expired_offers()

    def subscribe_received_payments(self, initial_index: int, stopped: threading.Event):
        with ReceivedPaymentsSubscriptionClient(
            self.squeak_store,
            initial_index,
            stopped,
        ).open_subscription() as client:
            yield from client.get_received_payments()

    def get_network(self) -> str:
        return self.config.node.network

    def get_squeak_entry(self, squeak_hash: bytes) -> Optional[SqueakEntry]:
        return self.squeak_store.get_squeak_entry(squeak_hash)

    def get_timeline_squeak_entries(
            self,
            limit: int,
            last_entry: Optional[SqueakEntry],
    ) -> List[SqueakEntry]:
        return self.squeak_store.get_timeline_squeak_entries(limit, last_entry)

    def get_liked_squeak_entries(
            self,
            limit: int,
            last_entry: Optional[SqueakEntry],
    ) -> List[SqueakEntry]:
        return self.squeak_store.get_liked_squeak_entries(limit, last_entry)

    def get_squeak_entries_for_public_key(
            self,
            public_key: SqueakPublicKey,
            limit: int,
            last_entry: Optional[SqueakEntry],
    ) -> List[SqueakEntry]:
        return self.squeak_store.get_squeak_entries_for_public_key(
            public_key,
            limit,
            last_entry,
        )

    def get_squeak_entries_for_text_search(
            self,
            search_text: str,
            limit: int,
            last_entry: Optional[SqueakEntry],
    ) -> List[SqueakEntry]:
        return self.squeak_store.get_squeak_entries_for_text_search(
            search_text,
            limit,
            last_entry,
        )

    def get_ancestor_squeak_entries(self, squeak_hash: bytes) -> List[SqueakEntry]:
        return self.squeak_store.get_ancestor_squeak_entries(squeak_hash)

    def get_reply_squeak_entries(
            self,
            squeak_hash: bytes,
            limit: int,
            last_entry: Optional[SqueakEntry],
    ) -> List[SqueakEntry]:
        return self.squeak_store.get_reply_squeak_entries(
            squeak_hash,
            limit,
            last_entry,
        )

    def get_received_payment_summary(self) -> ReceivedPaymentSummary:
        return self.squeak_store.get_received_payment_summary()

    def get_sent_payment_summary(self) -> SentPaymentSummary:
        return self.squeak_store.get_sent_payment_summary()

    def reprocess_received_payments(self) -> None:
        self.squeak_store.clear_received_payment_settle_indices()
        self.payment_processor.start_processing()

    def delete_old_squeaks(self):
        return self.squeak_store.delete_old_squeaks()

    def like_squeak(self, squeak_hash: bytes):
        self.squeak_store.like_squeak(squeak_hash)

    def unlike_squeak(self, squeak_hash: bytes):
        return self.squeak_store.unlike_squeak(squeak_hash)

    def connect_peer(self, peer_address: PeerAddress) -> None:
        logger.info("Connect to peer: {}".format(
            peer_address,
        ))
        self.network_manager.connect_peer_sync(peer_address)

    def get_connected_peer(self, peer_address: PeerAddress) -> Optional[ConnectedPeer]:
        peer = self.network_manager.get_connected_peer(peer_address)
        if peer is None:
            return None
        return ConnectedPeer(
            peer=peer,
            saved_peer=self.squeak_store.get_peer_by_address(
                peer_address,
            ),
        )

    def get_connected_peers(self) -> List[ConnectedPeer]:
        peers = self.network_manager.get_connected_peers()
        return [
            ConnectedPeer(
                peer=peer,
                saved_peer=self.squeak_store.get_peer_by_address(
                    peer.remote_address,
                ),
            ) for peer in peers
        ]

    def download_squeaks(
            self,
            public_keys: List[SqueakPublicKey],
            min_block: int,
            max_block: int,
            replyto_hash: Optional[bytes],
    ) -> DownloadResult:
        interest = CInterested(
            pubkeys=public_keys,
            nMinBlockHeight=min_block,
            nMaxBlockHeight=max_block,
            replyto_squeak_hash=replyto_hash,
        ) if replyto_hash else CInterested(
            pubkeys=public_keys,
            nMinBlockHeight=min_block,
            nMaxBlockHeight=max_block,
        )
        return self.active_download_manager.download_interest(10, interest)

    def download_single_squeak(self, squeak_hash: bytes) -> DownloadResult:
        logger.info("Downloading single squeak: {}".format(
            squeak_hash.hex(),
        ))
        return self.active_download_manager.download_hash(squeak_hash)

    def download_offers(self, squeak_hash: bytes) -> DownloadResult:
        logger.info("Downloading offers for squeak: {}".format(
            squeak_hash.hex(),
        ))
        return self.active_download_manager.download_offers(10, squeak_hash)

    def request_offers(self, squeak_hash: bytes):
        logger.info("Requesting offers for squeak: {}".format(
            squeak_hash.hex(),
        ))
        invs = [
            CInv(type=2, hash=squeak_hash)
        ]
        getdata_msg = msg_getdata(inv=invs)
        self.broadcast_msg(getdata_msg)

    def download_replies(self, squeak_hash: bytes) -> DownloadResult:
        logger.info("Downloading replies for squeak: {}".format(
            squeak_hash.hex(),
        ))
        interest = CInterested(
            hashReplySqk=squeak_hash,
        )
        return self.active_download_manager.download_interest(10, interest)

    def download_public_key_squeaks(self, public_key: SqueakPublicKey) -> DownloadResult:
        logger.info("Downloading squeaks for public key: {}".format(
            public_key,
        ))
        interest = CInterested(
            pubkeys=[public_key],
        )
        return self.active_download_manager.download_interest(10, interest)

    def broadcast_msg(self, msg: MsgSerializable) -> int:
        return self.network_manager.broadcast_msg(msg)

    def disconnect_peer(self, peer_address: PeerAddress) -> None:
        logger.info("Disconnect to peer: {}".format(
            peer_address,
        ))
        self.network_manager.disconnect_peer(peer_address)

    def subscribe_connected_peers(self, stopped: threading.Event) -> Iterable[List[ConnectedPeer]]:
        for peers in self.network_manager.subscribe_connected_peers(stopped):
            yield [
                ConnectedPeer(
                    peer=peer,
                    saved_peer=self.squeak_store.get_peer_by_address(
                        peer.remote_address,
                    )
                ) for peer in peers
            ]

    def subscribe_connected_peer(self, peer_address: PeerAddress, stopped: threading.Event) -> Iterable[Optional[ConnectedPeer]]:
        for peer in self.network_manager.subscribe_connected_peer(peer_address, stopped):
            if peer is None:
                yield None
            else:
                yield ConnectedPeer(
                    peer=peer,
                    saved_peer=self.squeak_store.get_peer_by_address(
                        peer.remote_address,
                    )
                )

    def subscribe_new_squeaks(self, stopped: threading.Event):
        yield from self.squeak_store.subscribe_new_squeaks(stopped)

    def subscribe_new_secret_keys(self, stopped: threading.Event):
        yield from self.squeak_store.subscribe_new_secret_keys(stopped)

    def subscribe_follows(self, stopped: threading.Event):
        yield from self.squeak_store.subscribe_follows(stopped)

    def subscribe_received_offers_for_squeak(self, squeak_hash: bytes, stopped: threading.Event):
        yield from self.squeak_store.subscribe_received_offers_for_squeak(
            squeak_hash,
            stopped,
        )

    def subscribe_squeak_entry(self, squeak_hash: bytes, stopped: threading.Event):
        for item in self.squeak_store.subscribe_new_squeaks(stopped):
            if squeak_hash == get_hash(item):
                yield self.get_squeak_entry(squeak_hash)

    def subscribe_squeak_reply_entries(self, squeak_hash: bytes, stopped: threading.Event):
        for item in self.squeak_store.subscribe_new_squeaks(stopped):
            if squeak_hash == item.hashReplySqk:
                reply_hash = get_hash(item)
                yield self.get_squeak_entry(reply_hash)

    def subscribe_squeak_public_key_entries(self, public_key: SqueakPublicKey, stopped: threading.Event):
        for item in self.squeak_store.subscribe_new_squeaks(stopped):
            if public_key == item.GetPubKey():
                squeak_hash = get_hash(item)
                yield self.get_squeak_entry(squeak_hash)

    def subscribe_squeak_ancestor_entries(self, squeak_hash: bytes, stopped: threading.Event):
        for item in self.squeak_store.subscribe_new_squeaks(stopped):
            if squeak_hash == get_hash(item):
                yield self.get_ancestor_squeak_entries(squeak_hash)

    def subscribe_squeak_entries(self, stopped: threading.Event):
        for item in self.squeak_store.subscribe_new_squeaks(stopped):
            squeak_hash = get_hash(item)
            yield self.get_squeak_entry(squeak_hash)

    def subscribe_timeline_squeak_entries(self, stopped: threading.Event):
        for item in self.squeak_store.subscribe_new_squeaks(stopped):
            followed_public_keys = self.squeak_store.get_followed_public_keys()
            if item.GetPubKey() in set(followed_public_keys):
                squeak_hash = get_hash(item)
                yield self.get_squeak_entry(squeak_hash)

    def get_external_address(self) -> PeerAddress:
        return self.network_manager.external_address

    def get_default_peer_port(self) -> int:
        return squeak.params.params.DEFAULT_PORT

    def set_sell_price_msat(self, sell_price_msat: int) -> None:
        self.node_settings.set_sell_price_msat(sell_price_msat)

    def clear_sell_price_msat(self) -> None:
        self.node_settings.clear_sell_price_msat()

    def get_sell_price_msat(self) -> Optional[int]:
        return self.node_settings.get_sell_price_msat()

    def get_default_sell_price_msat(self) -> int:
        return self.config.node.price_msat

    def add_twitter_account(self, handle: str, profile_id: int, bearer_token: str) -> Optional[int]:
        twitter_account_id = self.squeak_store.add_twitter_account(
            handle,
            profile_id,
            bearer_token,
        )
        self.update_twitter_stream()
        return twitter_account_id

    def get_twitter_accounts(self) -> List[TwitterAccountEntry]:
        return self.squeak_store.get_twitter_accounts()

    def delete_twitter_account(self, twitter_account_id: int) -> None:
        self.squeak_store.delete_twitter_account(twitter_account_id)
        self.update_twitter_stream()

    def update_twitter_stream(self) -> None:
        self.tweet_forwarder.start_processing()
