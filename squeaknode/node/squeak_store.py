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

from squeak.core import CSqueak
from squeak.core.signing import SqueakPrivateKey
from squeak.core.signing import SqueakPublicKey

from squeaknode.core.peer_address import PeerAddress
from squeaknode.core.peers import create_saved_peer
from squeaknode.core.profiles import create_contact_profile
from squeaknode.core.profiles import create_signing_profile
from squeaknode.core.profiles import get_profile_private_key
from squeaknode.core.received_offer import ReceivedOffer
from squeaknode.core.received_payment import ReceivedPayment
from squeaknode.core.sent_offer import SentOffer
from squeaknode.core.sent_payment import SentPayment
from squeaknode.core.squeak_entry import SqueakEntry
from squeaknode.core.squeak_peer import SqueakPeer
from squeaknode.core.squeak_profile import SqueakProfile
from squeaknode.core.update_subscriptions_event import UpdateSubscriptionsEvent
from squeaknode.node.listener_subscription_client import EventListener


logger = logging.getLogger(__name__)


class SqueakStore:

    def __init__(
        self,
        squeak_db,
        max_squeaks,
        max_squeaks_per_public_key_per_block,
    ):
        self.squeak_db = squeak_db
        self.max_squeaks = max_squeaks
        self.max_squeaks_per_public_key_per_block = max_squeaks_per_public_key_per_block,
        self.new_squeak_listener = EventListener()
        self.new_received_offer_listener = EventListener()
        self.new_secret_key_listener = EventListener()
        self.new_follow_listener = EventListener()
        self.twitter_stream_change_listener = EventListener()

    def save_squeak(self, squeak: CSqueak, block_header) -> Optional[bytes]:
        # Check if limit exceeded.
        if self.squeak_db.get_number_of_squeaks() >= self.max_squeaks:
            raise Exception("Exceeded max number of squeaks.")
        # TODO: Check if limit per public key per block is exceeded.
        # Insert the squeak in db.
        inserted_squeak_hash = self.squeak_db.insert_squeak(
            squeak,
            block_header,
        )
        if inserted_squeak_hash is None:
            return None
        logger.info("Saved squeak: {}".format(
            inserted_squeak_hash.hex(),
        ))
        # Notify the listener
        self.new_squeak_listener.handle_new_item(squeak)
        return inserted_squeak_hash

    def unlock_squeak(self, squeak_hash: bytes, secret_key: bytes, decrypted_content: str):
        squeak = self.squeak_db.get_squeak(squeak_hash)
        self.squeak_db.set_squeak_decryption_key(
            squeak_hash,
            secret_key,
            decrypted_content,
        )
        logger.info("Unlocked squeak: {}".format(
            squeak_hash.hex(),
        ))
        # Notify the listener
        self.new_secret_key_listener.handle_new_item(squeak)

    def get_squeak(self, squeak_hash: bytes) -> Optional[CSqueak]:
        return self.squeak_db.get_squeak(squeak_hash)

    def get_squeak_secret_key(self, squeak_hash: bytes) -> Optional[bytes]:
        return self.squeak_db.get_squeak_secret_key(squeak_hash)

    # def get_free_squeak_secret_key_reply(self, squeak_hash: bytes) -> Optional[FreeSecretKeyReply]:
    #     secret_key = self.get_squeak_secret_key(squeak_hash)
    #     if secret_key is None:
    #         return None
    #     return FreeSecretKeyReply(
    #         squeak_hash=squeak_hash,
    #         secret_key=secret_key,
    #     )

    def delete_squeak(self, squeak_hash: bytes) -> None:
        self.squeak_db.delete_squeak(squeak_hash)

    # def get_secret_key_reply(
    #         self,
    #         squeak_hash: bytes,
    #         peer_address: PeerAddress,
    #         price_msat: int,
    #         lnd_external_address: Optional[LightningAddressHostPort],
    # ) -> Optional[SecretKeyReply]:
    #     squeak = self.get_squeak(squeak_hash)
    #     if squeak is None:
    #         return None
    #     if price_msat == 0:
    #         return self.get_free_squeak_secret_key_reply(squeak_hash)
    #     else:
    #         return self.get_offer_reply(
    #             squeak=squeak,
    #             peer_address=peer_address,
    #             price_msat=price_msat,
    #             lnd_external_address=lnd_external_address,
    #         )

    def save_sent_offer(self, sent_offer: SentOffer) -> int:
        return self.squeak_db.insert_sent_offer(sent_offer)

    def get_sent_offer_for_peer(self, squeak_hash: bytes, peer_address: PeerAddress) -> Optional[SentOffer]:
        return self.squeak_db.get_sent_offer_by_squeak_hash_and_peer(
            squeak_hash,
            peer_address,
        )

    def create_signing_profile(self, profile_name: str) -> int:
        squeak_profile = create_signing_profile(
            profile_name,
        )
        profile_id = self.squeak_db.insert_profile(squeak_profile)
        self.create_update_subscriptions_event()
        return profile_id

    def import_signing_profile(self, profile_name: str, private_key: SqueakPrivateKey) -> int:
        squeak_profile = create_signing_profile(
            profile_name,
            private_key,
        )
        profile_id = self.squeak_db.insert_profile(squeak_profile)
        self.create_update_subscriptions_event()
        return profile_id

    def create_contact_profile(self, profile_name: str, public_key: SqueakPublicKey) -> int:
        squeak_profile = create_contact_profile(
            profile_name,
            public_key,
        )
        profile_id = self.squeak_db.insert_profile(squeak_profile)
        self.create_update_subscriptions_event()
        return profile_id

    def get_profiles(self) -> List[SqueakProfile]:
        return self.squeak_db.get_profiles()

    def get_signing_profiles(self) -> List[SqueakProfile]:
        return self.squeak_db.get_signing_profiles()

    def get_contact_profiles(self) -> List[SqueakProfile]:
        return self.squeak_db.get_contact_profiles()

    def get_squeak_profile(self, profile_id: int) -> Optional[SqueakProfile]:
        return self.squeak_db.get_profile(profile_id)

    def get_squeak_profile_by_public_key(self, public_key: SqueakPublicKey) -> Optional[SqueakProfile]:
        return self.squeak_db.get_profile_by_public_key(public_key)

    def get_squeak_profile_by_name(self, name: str) -> Optional[SqueakProfile]:
        return self.squeak_db.get_profile_by_name(name)

    def set_squeak_profile_following(self, profile_id: int, following: bool) -> None:
        self.squeak_db.set_profile_following(profile_id, following)
        self.create_update_subscriptions_event()

    def rename_squeak_profile(self, profile_id: int, profile_name: str) -> None:
        self.squeak_db.set_profile_name(profile_id, profile_name)

    def delete_squeak_profile(self, profile_id: int) -> None:
        self.squeak_db.delete_profile(profile_id)
        self.create_update_subscriptions_event()

    def set_squeak_profile_image(self, profile_id: int, profile_image: bytes) -> None:
        self.squeak_db.set_profile_image(profile_id, profile_image)

    def clear_squeak_profile_image(self, profile_id: int) -> None:
        self.squeak_db.set_profile_image(profile_id, None)

    def get_squeak_profile_private_key(self, profile_id: int) -> bytes:
        profile = self.get_squeak_profile(profile_id)
        if profile is None:
            raise Exception("Profile with id: {} does not exist.".format(
                profile_id,
            ))
        return get_profile_private_key(profile)

    def create_peer(self, peer_name: str, peer_address: PeerAddress):
        squeak_peer = create_saved_peer(
            peer_name,
            peer_address,
        )
        return self.squeak_db.insert_peer(squeak_peer)

    def get_peer(self, peer_id: int) -> Optional[SqueakPeer]:
        return self.squeak_db.get_peer(peer_id)

    def get_peer_by_address(self, peer_address: PeerAddress) -> Optional[SqueakPeer]:
        return self.squeak_db.get_peer_by_address(peer_address)

    def get_peers(self):
        return self.squeak_db.get_peers()

    def get_autoconnect_peers(self) -> List[SqueakPeer]:
        return self.squeak_db.get_autoconnect_peers()

    def set_peer_autoconnect(self, peer_id: int, autoconnect: bool):
        self.squeak_db.set_peer_autoconnect(peer_id, autoconnect)

    def set_peer_share_for_free(self, peer_id: int, share_for_free: bool):
        self.squeak_db.set_peer_share_for_free(peer_id, share_for_free)

    def rename_peer(self, peer_id: int, peer_name: str):
        self.squeak_db.set_peer_name(peer_id, peer_name)

    def delete_peer(self, peer_id: int):
        self.squeak_db.delete_peer(peer_id)

    def get_received_offers(self, squeak_hash: bytes) -> List[ReceivedOffer]:
        return self.squeak_db.get_received_offers(squeak_hash)

    def get_received_offer(self, received_offer_id: int) -> Optional[ReceivedOffer]:
        return self.squeak_db.get_received_offer(received_offer_id)

    def save_sent_payment(self, sent_payment: SentPayment) -> int:
        return self.squeak_db.insert_sent_payment(sent_payment)

    def get_sent_payments(
            self,
            limit: int,
            last_sent_payment: Optional[SentPayment],
    ) -> List[SentPayment]:
        return self.squeak_db.get_sent_payments(
            limit,
            last_sent_payment,
        )

    def get_sent_payment(self, sent_payment_id: int) -> Optional[SentPayment]:
        return self.squeak_db.get_sent_payment(sent_payment_id)

    def get_sent_offers(self):
        return self.squeak_db.get_sent_offers()

    def mark_received_offer_paid(self, payment_hash: bytes) -> None:
        self.squeak_db.set_received_offer_paid(payment_hash, True)

    def get_received_payments(
            self,
            limit: int,
            last_received_payment: Optional[ReceivedPayment],
    ) -> List[ReceivedPayment]:
        return self.squeak_db.get_received_payments(
            limit,
            last_received_payment,
        )

    # def delete_all_expired_offers(self):
    #     self.delete_all_expired_received_offers()
    #     self.delete_all_expired_sent_offers()

    # def delete_all_expired_received_offers(self):
    #     received_offer_retention_s = self.config.node.received_offer_retention_s
    #     num_expired_received_offers = self.squeak_db.delete_expired_received_offers(
    #         received_offer_retention_s)
    #     if num_expired_received_offers > 0:
    #         logger.info("Deleted number of expired received offers: {}".format(
    #             num_expired_received_offers))

    # def delete_all_expired_sent_offers(self):
    #     sent_offer_retention_s = self.config.node.sent_offer_retention_s
    #     num_expired_sent_offers = self.squeak_db.delete_expired_sent_offers(
    #         sent_offer_retention_s,
    #     )
    #     if num_expired_sent_offers > 0:
    #         logger.info(
    #             "Deleted number of expired sent offers: {}".format(
    #                 num_expired_sent_offers)
    #         )

    # def subscribe_received_payments(self, initial_index: int, stopped: threading.Event):
    #     with ReceivedPaymentsSubscriptionClient(
    #         self.squeak_db,
    #         initial_index,
    #         stopped,
    #     ).open_subscription() as client:
    #         yield from client.get_received_payments()

    # def get_block_range(self) -> BlockRange:
    #     max_block = self.squeak_core.get_best_block_height()
    #     block_interval = self.interest_block_interval
    #     min_block = max(0, max_block - block_interval)
    #     return BlockRange(min_block, max_block)

    def get_squeak_entry(self, squeak_hash: bytes) -> Optional[SqueakEntry]:
        return self.squeak_db.get_squeak_entry(squeak_hash)

    # def get_timeline_squeak_entries(
    #         self,
    #         limit: int,
    #         last_entry: Optional[SqueakEntry],
    # ) -> List[SqueakEntry]:
    #     return self.squeak_db.get_timeline_squeak_entries(
    #         limit,
    #         last_entry,
    #     )

    # def get_liked_squeak_entries(
    #         self,
    #         limit: int,
    #         last_entry: Optional[SqueakEntry],
    # ) -> List[SqueakEntry]:
    #     return self.squeak_db.get_liked_squeak_entries(
    #         limit,
    #         last_entry,
    #     )

    # def get_squeak_entries_for_public_key(
    #         self,
    #         public_key: SqueakPublicKey,
    #         limit: int,
    #         last_entry: Optional[SqueakEntry],
    # ) -> List[SqueakEntry]:
    #     return self.squeak_db.get_squeak_entries_for_public_key(
    #         public_key,
    #         limit,
    #         last_entry,
    #     )

    # def get_squeak_entries_for_text_search(
    #         self,
    #         search_text: str,
    #         limit: int,
    #         last_entry: Optional[SqueakEntry],
    # ) -> List[SqueakEntry]:
    #     return self.squeak_db.get_squeak_entries_for_text_search(
    #         search_text,
    #         limit,
    #         last_entry,
    #     )

    # def get_ancestor_squeak_entries(self, squeak_hash: bytes) -> List[SqueakEntry]:
    #     return self.squeak_db.get_thread_ancestor_squeak_entries(
    #         squeak_hash,
    #     )

    # def get_reply_squeak_entries(
    #         self,
    #         squeak_hash: bytes,
    #         limit: int,
    #         last_entry: Optional[SqueakEntry],
    # ) -> List[SqueakEntry]:
    #     return self.squeak_db.get_thread_reply_squeak_entries(
    #         squeak_hash,
    #         limit,
    #         last_entry,
    #     )

    # def get_number_of_squeaks(self) -> int:
    #     return self.squeak_db.get_number_of_squeaks()

    # def save_received_offer(self, offer: Offer, peer_address: PeerAddress) -> Optional[int]:
    #     squeak = self.get_squeak(offer.squeak_hash)
    #     secret_key = self.get_squeak_secret_key(offer.squeak_hash)
    #     if squeak is None or secret_key is not None:
    #         return None
    #     try:
    #         # TODO: Call unpack_offer with check_payment_point=True.
    #         received_offer = self.squeak_core.unpack_offer(
    #             squeak,
    #             offer,
    #             peer_address,
    #         )
    #     except Exception:
    #         logger.exception("Failed to save received offer.")
    #         return None
    #     received_offer_id = self.squeak_db.insert_received_offer(
    #         received_offer)
    #     if received_offer_id is None:
    #         return None
    #     logger.info("Saved received offer: {}".format(received_offer))
    #     received_offer = received_offer._replace(
    #         received_offer_id=received_offer_id)
    #     self.new_received_offer_listener.handle_new_item(received_offer)
    #     return received_offer_id

    # def get_followed_public_keys(self) -> List[SqueakPublicKey]:
    #     followed_profiles = self.squeak_db.get_following_profiles()
    #     return [profile.public_key for profile in followed_profiles]

    # def get_received_payment_summary(self) -> ReceivedPaymentSummary:
    #     return self.squeak_db.get_received_payment_summary()

    # def get_sent_payment_summary(self) -> SentPaymentSummary:
    #     return self.squeak_db.get_sent_payment_summary()

    # def clear_received_payment_settle_indices(self) -> None:
    #     self.squeak_db.clear_received_payment_settle_indices()

    # def delete_old_squeaks(self):
    #     squeaks_to_delete = self.squeak_db.get_old_squeaks_to_delete(
    #         self.config.node.squeak_retention_s,
    #     )
    #     for squeak_hash in squeaks_to_delete:
    #         self.squeak_db.delete_squeak(
    #             squeak_hash,
    #         )
    #         logger.info("Deleted squeak: {}".format(
    #             squeak_hash.hex(),
    #         ))

    # def like_squeak(self, squeak_hash: bytes):
    #     logger.info("Liking squeak: {}".format(
    #         squeak_hash.hex(),
    #     ))
    #     self.squeak_db.set_squeak_liked(
    #         squeak_hash,
    #     )

    # def unlike_squeak(self, squeak_hash: bytes):
    #     logger.info("Unliking squeak: {}".format(
    #         squeak_hash.hex(),
    #     ))
    #     self.squeak_db.set_squeak_unliked(
    #         squeak_hash,
    #     )

    # def lookup_squeaks(
    #         self,
    #         public_keys: List[SqueakPublicKey],
    #         min_block: Optional[int],
    #         max_block: Optional[int],
    #         reply_to_hash: Optional[bytes],
    # ) -> List[bytes]:
    #     return self.squeak_db.lookup_squeaks(
    #         public_keys,
    #         min_block,
    #         max_block,
    #         reply_to_hash,
    #         include_locked=True,
    #     )

    # def lookup_secret_keys(
    #         self,
    #         public_keys: List[SqueakPublicKey],
    #         min_block: Optional[int],
    #         max_block: Optional[int],
    #         reply_to_hash: Optional[bytes],
    # ) -> List[bytes]:
    #     return self.squeak_db.lookup_squeaks(
    #         public_keys,
    #         min_block,
    #         max_block,
    #         reply_to_hash,
    #     )

    def subscribe_new_squeaks(self, stopped: threading.Event):
        yield from self.new_squeak_listener.yield_items(stopped)

    def subscribe_new_secret_keys(self, stopped: threading.Event):
        yield from self.new_secret_key_listener.yield_items(stopped)

    def subscribe_follows(self, stopped: threading.Event):
        yield from self.new_follow_listener.yield_items(stopped)

    def create_update_subscriptions_event(self):
        self.new_follow_listener.handle_new_item(UpdateSubscriptionsEvent())

    # def subscribe_received_offers_for_squeak(self, squeak_hash: bytes, stopped: threading.Event):
    #     for received_offer in self.new_received_offer_listener.yield_items(stopped):
    #         if received_offer.squeak_hash == squeak_hash:
    #             yield received_offer

    # def subscribe_squeak_entry(self, squeak_hash: bytes, stopped: threading.Event):
    #     for item in self.new_squeak_listener.yield_items(stopped):
    #         if squeak_hash == get_hash(item):
    #             yield self.get_squeak_entry(squeak_hash)

    # def subscribe_squeak_reply_entries(self, squeak_hash: bytes, stopped: threading.Event):
    #     for item in self.new_squeak_listener.yield_items(stopped):
    #         if squeak_hash == item.hashReplySqk:
    #             reply_hash = get_hash(item)
    #             yield self.get_squeak_entry(reply_hash)

    # def subscribe_squeak_public_key_entries(self, public_key: SqueakPublicKey, stopped: threading.Event):
    #     for item in self.new_squeak_listener.yield_items(stopped):
    #         if public_key == item.GetPubKey():
    #             squeak_hash = get_hash(item)
    #             yield self.get_squeak_entry(squeak_hash)

    # def subscribe_squeak_ancestor_entries(self, squeak_hash: bytes, stopped: threading.Event):
    #     for item in self.new_squeak_listener.yield_items(stopped):
    #         if squeak_hash == get_hash(item):
    #             yield self.get_ancestor_squeak_entries(squeak_hash)

    # def subscribe_squeak_entries(self, stopped: threading.Event):
    #     for item in self.new_squeak_listener.yield_items(stopped):
    #         squeak_hash = get_hash(item)
    #         yield self.get_squeak_entry(squeak_hash)

    # def subscribe_timeline_squeak_entries(self, stopped: threading.Event):
    #     for item in self.new_squeak_listener.yield_items(stopped):
    #         followed_public_keys = self.get_followed_public_keys()
    #         if item.GetPubKey() in set(followed_public_keys):
    #             squeak_hash = get_hash(item)
    #             yield self.get_squeak_entry(squeak_hash)

    # def create_update_twitter_stream_event(self):
    #     self.twitter_stream_change_listener.handle_new_item(
    #         UpdateTwitterStreamEvent()
    #     )

    # def add_twitter_account(self, handle: str, profile_id: int) -> Optional[int]:
    #     twitter_account = TwitterAccount(
    #         twitter_account_id=None,
    #         handle=handle,
    #         profile_id=profile_id,
    #     )
    #     account_id = self.squeak_db.insert_twitter_account(twitter_account)
    #     self.create_update_twitter_stream_event()
    #     return account_id

    # def get_twitter_accounts(self) -> List[TwitterAccountEntry]:
    #     return self.squeak_db.get_twitter_accounts()

    # def delete_twitter_account(self, twitter_account_id: int) -> None:
    #     self.squeak_db.delete_twitter_account(twitter_account_id)
    #     self.create_update_twitter_stream_event()