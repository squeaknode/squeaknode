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
from squeak.core.signing import SqueakPrivateKey
from squeak.core.signing import SqueakPublicKey
from squeak.messages import msg_getdata
from squeak.messages import msg_inv
from squeak.messages import MSG_SECRET_KEY
from squeak.messages import MSG_SQUEAK
from squeak.messages import MsgSerializable
from squeak.net import CInterested
from squeak.net import CInv
from squeak.net import CSqueakLocator

from squeaknode.core.block_range import BlockRange
from squeaknode.core.connected_peer import ConnectedPeer
from squeaknode.core.download_result import DownloadResult
from squeaknode.core.lightning_address import LightningAddressHostPort
from squeaknode.core.offer import Offer
from squeaknode.core.peer_address import PeerAddress
from squeaknode.core.peers import create_saved_peer
from squeaknode.core.profiles import create_contact_profile
from squeaknode.core.profiles import create_signing_profile
from squeaknode.core.profiles import get_profile_private_key
from squeaknode.core.received_offer import ReceivedOffer
from squeaknode.core.received_payment import ReceivedPayment
from squeaknode.core.received_payment_summary import ReceivedPaymentSummary
from squeaknode.core.sent_offer import SentOffer
from squeaknode.core.sent_payment import SentPayment
from squeaknode.core.sent_payment_summary import SentPaymentSummary
from squeaknode.core.squeak_entry import SqueakEntry
from squeaknode.core.squeak_peer import SqueakPeer
from squeaknode.core.squeak_profile import SqueakProfile
from squeaknode.core.squeaks import get_hash
from squeaknode.core.twitter_account import TwitterAccount
from squeaknode.core.twitter_account_entry import TwitterAccountEntry
from squeaknode.core.update_subscriptions_event import UpdateSubscriptionsEvent
from squeaknode.core.update_twitter_stream_event import UpdateTwitterStreamEvent
from squeaknode.core.user_config import UserConfig
from squeaknode.node.active_download_manager import ActiveDownload
from squeaknode.node.downloaded_object import DownloadedOffer
from squeaknode.node.downloaded_object import DownloadedSqueak
from squeaknode.node.listener_subscription_client import EventListener
from squeaknode.node.price_policy import PricePolicy
from squeaknode.node.received_payments_subscription_client import ReceivedPaymentsSubscriptionClient
from squeaknode.node.secret_key_reply import FreeSecretKeyReply
from squeaknode.node.secret_key_reply import OfferReply
from squeaknode.node.secret_key_reply import SecretKeyReply


logger = logging.getLogger(__name__)


class SqueakController:

    def __init__(
        self,
        squeak_db,
        squeak_core,
        payment_processor,
        network_manager,
        download_manager,
        tweet_forwarder,
        config,
    ):
        self.squeak_db = squeak_db
        self.squeak_core = squeak_core
        self.payment_processor = payment_processor
        self.network_manager = network_manager
        self.new_squeak_listener = EventListener()
        self.new_received_offer_listener = EventListener()
        self.new_secret_key_listener = EventListener()
        self.new_follow_listener = EventListener()
        self.twitter_stream_change_listener = EventListener()
        self.active_download_manager = download_manager
        self.tweet_forwarder = tweet_forwarder
        self.config = config

    def save_squeak(self, squeak: CSqueak) -> Optional[bytes]:
        # Check if the squeak is valid
        self.squeak_core.check_squeak(squeak)
        # Get the block header for the squeak.
        block_header = self.squeak_core.get_block_header(squeak)
        # Check if limit exceeded.
        if self.get_number_of_squeaks() >= self.config.node.max_squeaks:
            raise Exception("Exceeded max number of squeaks.")
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

    def unlock_squeak(self, squeak_hash: bytes, secret_key: bytes):
        squeak = self.squeak_db.get_squeak(squeak_hash)
        decrypted_content = self.squeak_core.get_decrypted_content(
            squeak,
            secret_key,
        )
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

    def make_squeak(self, profile_id: int, content_str: str, replyto_hash: Optional[bytes]) -> Optional[bytes]:
        squeak_profile = self.squeak_db.get_profile(profile_id)
        squeak, decryption_key = self.squeak_core.make_squeak(
            squeak_profile, content_str, replyto_hash)
        inserted_squeak_hash = self.save_squeak(squeak)
        if inserted_squeak_hash is None:
            return None
        self.unlock_squeak(
            inserted_squeak_hash,
            decryption_key,
        )
        return inserted_squeak_hash

    def get_squeak(self, squeak_hash: bytes) -> Optional[CSqueak]:
        return self.squeak_db.get_squeak(squeak_hash)

    def get_squeak_secret_key(self, squeak_hash: bytes) -> Optional[bytes]:
        return self.squeak_db.get_squeak_secret_key(squeak_hash)

    def get_free_squeak_secret_key_reply(self, squeak_hash: bytes) -> Optional[FreeSecretKeyReply]:
        secret_key = self.get_squeak_secret_key(squeak_hash)
        if secret_key is None:
            return None
        return FreeSecretKeyReply(
            squeak_hash=squeak_hash,
            secret_key=secret_key,
        )

    def delete_squeak(self, squeak_hash: bytes) -> None:
        self.squeak_db.delete_squeak(squeak_hash)

    def squeak_in_limit_of_interest(self, squeak: CSqueak, interest: CInterested) -> bool:
        return self.squeak_db.number_of_squeaks_with_public_key_in_block_range(
            squeak.GetPubKey(),
            interest.nMinBlockHeight,
            interest.nMaxBlockHeight,
        ) < self.config.node.max_squeaks_per_address_in_block_range

    def get_download_squeak_counter(self, squeak: CSqueak) -> Optional[ActiveDownload]:
        downloaded_squeak = DownloadedSqueak(squeak)
        return self.active_download_manager.lookup_counter(downloaded_squeak)

    def get_download_offer_counter(self, offer: Offer) -> Optional[ActiveDownload]:
        downloaded_offer = DownloadedOffer(offer)
        return self.active_download_manager.lookup_counter(downloaded_offer)

    def get_secret_key_reply(self, squeak_hash: bytes, peer_address: PeerAddress) -> Optional[SecretKeyReply]:
        squeak = self.get_squeak(squeak_hash)
        if squeak is None:
            return None
        price = self.get_price_for_squeak(squeak, peer_address)
        if price == 0:
            return self.get_free_squeak_secret_key_reply(squeak_hash)
        else:
            return self.get_offer_reply(
                squeak=squeak,
                peer_address=peer_address,
                price_msat=price,
            )

    def get_offer_reply(self, squeak: CSqueak, peer_address: PeerAddress, price_msat: int) -> Optional[OfferReply]:
        sent_offer = self.get_sent_offer_for_peer(
            squeak,
            peer_address,
            price_msat,
        )
        if sent_offer is None:
            return None
        lnd_external_address: Optional[LightningAddressHostPort] = None
        if self.config.lnd.external_host:
            lnd_external_address = LightningAddressHostPort(
                host=self.config.lnd.external_host,
                port=self.config.lnd.port,
            )
        try:
            offer = self.squeak_core.package_offer(
                sent_offer,
                lnd_external_address,
            )
            return OfferReply(
                squeak_hash=get_hash(squeak),
                offer=offer,
            )
        except Exception:
            return None

    def get_sent_offer_for_peer(self, squeak: CSqueak, peer_address: PeerAddress, price_msat: int) -> Optional[SentOffer]:
        squeak_hash = get_hash(squeak)
        # Check if there is an existing offer for the hash/peer_address combination
        sent_offer = self.squeak_db.get_sent_offer_by_squeak_hash_and_peer(
            squeak_hash,
            peer_address,
        )
        if sent_offer:
            return sent_offer
        secret_key = self.get_squeak_secret_key(squeak_hash)
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
        self.squeak_db.insert_sent_offer(sent_offer)
        return sent_offer

    def get_price_for_squeak(self, squeak: CSqueak, peer_address: PeerAddress) -> int:
        price_policy = PricePolicy(self.squeak_db, self.config)
        return price_policy.get_price(squeak, peer_address)

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
        return self.squeak_db.get_received_offer(
            received_offer_id)

    def pay_offer(self, received_offer_id: int) -> int:
        # Get the offer from the database
        received_offer = self.squeak_db.get_received_offer(
            received_offer_id)
        if received_offer is None:
            raise Exception("Received offer with id {} not found.".format(
                received_offer_id,
            ))
        logger.info("Paying received offer: {}".format(received_offer))
        sent_payment = self.squeak_core.pay_offer(received_offer)
        sent_payment_id = self.squeak_db.insert_sent_payment(sent_payment)
        # # Delete the received offer
        # self.squeak_db.delete_offer(sent_payment.payment_hash)
        # Mark the received offer as paid
        self.squeak_db.set_received_offer_paid(
            sent_payment.payment_hash,
            paid=True,
        )
        self.unlock_squeak(
            received_offer.squeak_hash,
            sent_payment.secret_key,
        )
        return sent_payment_id

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

    def get_received_payments(
            self,
            limit: int,
            last_received_payment: Optional[ReceivedPayment],
    ) -> List[ReceivedPayment]:
        return self.squeak_db.get_received_payments(
            limit,
            last_received_payment,
        )

    def delete_all_expired_offers(self):
        self.delete_all_expired_received_offers()
        self.delete_all_expired_sent_offers()

    def delete_all_expired_received_offers(self):
        received_offer_retention_s = self.config.node.received_offer_retention_s
        num_expired_received_offers = self.squeak_db.delete_expired_received_offers(
            received_offer_retention_s)
        if num_expired_received_offers > 0:
            logger.info("Deleted number of expired received offers: {}".format(
                num_expired_received_offers))

    def delete_all_expired_sent_offers(self):
        sent_offer_retention_s = self.config.node.sent_offer_retention_s
        num_expired_sent_offers = self.squeak_db.delete_expired_sent_offers(
            sent_offer_retention_s,
        )
        if num_expired_sent_offers > 0:
            logger.info(
                "Deleted number of expired sent offers: {}".format(
                    num_expired_sent_offers)
            )

    def subscribe_received_payments(self, initial_index: int, stopped: threading.Event):
        with ReceivedPaymentsSubscriptionClient(
            self.squeak_db,
            initial_index,
            stopped,
        ).open_subscription() as client:
            yield from client.get_received_payments()

    def get_block_range(self) -> BlockRange:
        max_block = self.squeak_core.get_best_block_height()
        block_interval = self.config.node.interest_block_interval
        min_block = max(0, max_block - block_interval)
        return BlockRange(min_block, max_block)

    def get_network(self) -> str:
        return self.config.node.network

    def get_squeak_entry(self, squeak_hash: bytes) -> Optional[SqueakEntry]:
        return self.squeak_db.get_squeak_entry(squeak_hash)

    def get_timeline_squeak_entries(
            self,
            limit: int,
            last_entry: Optional[SqueakEntry],
    ) -> List[SqueakEntry]:
        return self.squeak_db.get_timeline_squeak_entries(
            limit,
            last_entry,
        )

    def get_liked_squeak_entries(
            self,
            limit: int,
            last_entry: Optional[SqueakEntry],
    ) -> List[SqueakEntry]:
        return self.squeak_db.get_liked_squeak_entries(
            limit,
            last_entry,
        )

    def get_squeak_entries_for_public_key(
            self,
            public_key: SqueakPublicKey,
            limit: int,
            last_entry: Optional[SqueakEntry],
    ) -> List[SqueakEntry]:
        return self.squeak_db.get_squeak_entries_for_public_key(
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
        return self.squeak_db.get_squeak_entries_for_text_search(
            search_text,
            limit,
            last_entry,
        )

    def get_ancestor_squeak_entries(self, squeak_hash: bytes) -> List[SqueakEntry]:
        return self.squeak_db.get_thread_ancestor_squeak_entries(
            squeak_hash,
        )

    def get_reply_squeak_entries(
            self,
            squeak_hash: bytes,
            limit: int,
            last_entry: Optional[SqueakEntry],
    ) -> List[SqueakEntry]:
        return self.squeak_db.get_thread_reply_squeak_entries(
            squeak_hash,
            limit,
            last_entry,
        )

    def get_number_of_squeaks(self) -> int:
        return self.squeak_db.get_number_of_squeaks()

    def save_received_offer(self, offer: Offer, peer_address: PeerAddress) -> Optional[int]:
        squeak = self.get_squeak(offer.squeak_hash)
        secret_key = self.get_squeak_secret_key(offer.squeak_hash)
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
        received_offer_id = self.squeak_db.insert_received_offer(
            received_offer)
        if received_offer_id is None:
            return None
        logger.info("Saved received offer: {}".format(received_offer))
        received_offer = received_offer._replace(
            received_offer_id=received_offer_id)
        self.new_received_offer_listener.handle_new_item(received_offer)
        return received_offer_id

    # def get_followed_addresses(self) -> List[str]:
    #     followed_profiles = self.squeak_db.get_following_profiles()
    #     return [profile.address for profile in followed_profiles]

    def get_followed_public_keys(self) -> List[SqueakPublicKey]:
        followed_profiles = self.squeak_db.get_following_profiles()
        return [profile.public_key for profile in followed_profiles]

    def get_received_payment_summary(self) -> ReceivedPaymentSummary:
        return self.squeak_db.get_received_payment_summary()

    def get_sent_payment_summary(self) -> SentPaymentSummary:
        return self.squeak_db.get_sent_payment_summary()

    def reprocess_received_payments(self) -> None:
        self.squeak_db.clear_received_payment_settle_indices()
        self.payment_processor.start_processing()

    def delete_old_squeaks(self):
        squeaks_to_delete = self.squeak_db.get_old_squeaks_to_delete(
            self.config.node.squeak_retention_s,
        )
        for squeak_hash in squeaks_to_delete:
            self.squeak_db.delete_squeak(
                squeak_hash,
            )
            logger.info("Deleted squeak: {}".format(
                squeak_hash.hex(),
            ))

    def like_squeak(self, squeak_hash: bytes):
        logger.info("Liking squeak: {}".format(
            squeak_hash.hex(),
        ))
        self.squeak_db.set_squeak_liked(
            squeak_hash,
        )

    def unlike_squeak(self, squeak_hash: bytes):
        logger.info("Unliking squeak: {}".format(
            squeak_hash.hex(),
        ))
        self.squeak_db.set_squeak_unliked(
            squeak_hash,
        )

    def connect_peer(self, peer_address: PeerAddress) -> None:
        logger.info("Connect to peer: {}".format(
            peer_address,
        ))
        self.network_manager.connect_peer_sync(peer_address)

    def connect_saved_peers(self) -> None:
        peers = self.get_autoconnect_peers()
        for peer in peers:
            self.network_manager.connect_peer_async(
                peer.address,
            )

    def get_connected_peer(self, peer_address: PeerAddress) -> Optional[ConnectedPeer]:
        peer = self.network_manager.get_connected_peer(peer_address)
        if peer is None:
            return None
        return ConnectedPeer(
            peer=peer,
            saved_peer=self.squeak_db.get_peer_by_address(
                peer_address,
            ),
        )

    def get_connected_peers(self) -> List[ConnectedPeer]:
        peers = self.network_manager.get_connected_peers()
        return [
            ConnectedPeer(
                peer=peer,
                saved_peer=self.squeak_db.get_peer_by_address(
                    peer.remote_address,
                ),
            ) for peer in peers
        ]

    def lookup_squeaks(
            self,
            public_keys: List[SqueakPublicKey],
            min_block: Optional[int],
            max_block: Optional[int],
            reply_to_hash: Optional[bytes],
    ) -> List[bytes]:
        return self.squeak_db.lookup_squeaks(
            public_keys,
            min_block,
            max_block,
            reply_to_hash,
            include_locked=True,
        )

    def lookup_secret_keys(
            self,
            public_keys: List[SqueakPublicKey],
            min_block: Optional[int],
            max_block: Optional[int],
            reply_to_hash: Optional[bytes],
    ) -> List[bytes]:
        return self.squeak_db.lookup_squeaks(
            public_keys,
            min_block,
            max_block,
            reply_to_hash,
        )

    def get_interested_locator(self) -> CSqueakLocator:
        block_range = self.get_block_range()
        followed_public_keys = self.get_followed_public_keys()
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
                    saved_peer=self.squeak_db.get_peer_by_address(
                        peer.remote_address,
                    ),
                ) for peer in peers
            ]

    def subscribe_connected_peer(self, peer_address: PeerAddress, stopped: threading.Event) -> Iterable[Optional[ConnectedPeer]]:
        for peer in self.network_manager.subscribe_connected_peer(peer_address, stopped):
            if peer is None:
                yield None
            else:
                yield ConnectedPeer(
                    peer=peer,
                    saved_peer=self.squeak_db.get_peer_by_address(
                        peer.remote_address,
                    ),
                )

    def subscribe_new_squeaks(self, stopped: threading.Event):
        yield from self.new_squeak_listener.yield_items(stopped)

    def subscribe_new_secret_keys(self, stopped: threading.Event):
        yield from self.new_secret_key_listener.yield_items(stopped)

    def subscribe_follows(self, stopped: threading.Event):
        yield from self.new_follow_listener.yield_items(stopped)

    def subscribe_twitter_stream_changes(self, stopped: threading.Event):
        yield from self.twitter_stream_change_listener.yield_items(stopped)

    def update_subscriptions(self):
        locator = self.get_interested_locator()
        self.network_manager.update_local_subscriptions(locator)

    def create_update_subscriptions_event(self):
        self.new_follow_listener.handle_new_item(UpdateSubscriptionsEvent())

    def create_update_twitter_stream_event(self):
        self.twitter_stream_change_listener.handle_new_item(
            UpdateTwitterStreamEvent()
        )

    def subscribe_received_offers_for_squeak(self, squeak_hash: bytes, stopped: threading.Event):
        for received_offer in self.new_received_offer_listener.yield_items(stopped):
            if received_offer.squeak_hash == squeak_hash:
                yield received_offer

    def subscribe_squeak_entry(self, squeak_hash: bytes, stopped: threading.Event):
        for item in self.new_squeak_listener.yield_items(stopped):
            if squeak_hash == get_hash(item):
                yield self.get_squeak_entry(squeak_hash)

    def subscribe_squeak_reply_entries(self, squeak_hash: bytes, stopped: threading.Event):
        for item in self.new_squeak_listener.yield_items(stopped):
            if squeak_hash == item.hashReplySqk:
                reply_hash = get_hash(item)
                yield self.get_squeak_entry(reply_hash)

    def subscribe_squeak_public_key_entries(self, public_key: SqueakPublicKey, stopped: threading.Event):
        for item in self.new_squeak_listener.yield_items(stopped):
            if public_key == item.GetPubKey():
                squeak_hash = get_hash(item)
                yield self.get_squeak_entry(squeak_hash)

    def subscribe_squeak_ancestor_entries(self, squeak_hash: bytes, stopped: threading.Event):
        for item in self.new_squeak_listener.yield_items(stopped):
            if squeak_hash == get_hash(item):
                yield self.get_ancestor_squeak_entries(squeak_hash)

    def subscribe_squeak_entries(self, stopped: threading.Event):
        for item in self.new_squeak_listener.yield_items(stopped):
            squeak_hash = get_hash(item)
            yield self.get_squeak_entry(squeak_hash)

    def subscribe_timeline_squeak_entries(self, stopped: threading.Event):
        for item in self.new_squeak_listener.yield_items(stopped):
            followed_public_keys = self.get_followed_public_keys()
            if item.GetPubKey() in set(followed_public_keys):
                squeak_hash = get_hash(item)
                yield self.get_squeak_entry(squeak_hash)

    def get_external_address(self) -> PeerAddress:
        return self.network_manager.external_address

    def get_default_peer_port(self) -> int:
        return squeak.params.params.DEFAULT_PORT

    def forward_squeak(self, squeak):
        logger.debug("Forward new squeak: {!r}".format(
            get_hash(squeak).hex(),
        ))
        for peer in self.network_manager.get_connected_peers():
            if peer.is_remote_subscribed(squeak):
                logger.debug("Forwarding to peer: {}".format(
                    peer,
                ))
                squeak_hash = get_hash(squeak)
                inv = CInv(type=MSG_SQUEAK, hash=squeak_hash)
                inv_msg = msg_inv(inv=[inv])
                peer.send_msg(inv_msg)
        logger.debug("Finished checking peers to forward.")

    def forward_secret_key(self, squeak):
        logger.debug("Forward new secret key for hash: {!r}".format(
            get_hash(squeak).hex(),
        ))
        for peer in self.network_manager.get_connected_peers():
            if peer.is_remote_subscribed(squeak):
                logger.debug("Forwarding to peer: {}".format(
                    peer,
                ))
                squeak_hash = get_hash(squeak)
                inv = CInv(type=MSG_SECRET_KEY, hash=squeak_hash)
                inv_msg = msg_inv(inv=[inv])
                peer.send_msg(inv_msg)
        logger.debug("Finished checking peers to forward.")

    def insert_user_config(self) -> Optional[str]:
        user_config = UserConfig(username=self.config.webadmin.username)
        return self.squeak_db.insert_config(user_config)

    def set_sell_price_msat(self, sell_price_msat: int) -> None:
        self.insert_user_config()
        if sell_price_msat < 0:
            raise Exception("Sell price cannot be negative.")
        self.squeak_db.set_config_sell_price_msat(
            username=self.config.webadmin.username,
            sell_price_msat=sell_price_msat,
        )

    def clear_sell_price_msat(self) -> None:
        self.insert_user_config()
        self.squeak_db.clear_config_sell_price_msat(
            username=self.config.webadmin.username,
        )

    def get_sell_price_msat(self) -> Optional[int]:
        user_config = self.squeak_db.get_config(
            username=self.config.webadmin.username,
        )
        if user_config is None:
            return None
        return user_config.sell_price_msat

    def get_default_sell_price_msat(self) -> int:
        return self.config.node.price_msat

    def set_twitter_bearer_token(self, twitter_bearer_token: str) -> None:
        self.insert_user_config()
        self.squeak_db.set_config_twitter_bearer_token(
            username=self.config.webadmin.username,
            twitter_bearer_token=twitter_bearer_token,
        )
        self.create_update_twitter_stream_event()

    def get_twitter_bearer_token(self) -> Optional[str]:
        user_config = self.squeak_db.get_config(
            username=self.config.webadmin.username,
        )
        if user_config is None:
            return None
        return user_config.twitter_bearer_token

    def get_twitter_stream_status(self) -> bool:
        return self.tweet_forwarder.is_processing()

    def add_twitter_account(self, handle: str, profile_id: int) -> Optional[int]:
        twitter_account = TwitterAccount(
            twitter_account_id=None,
            handle=handle,
            profile_id=profile_id,
        )
        account_id = self.squeak_db.insert_twitter_account(twitter_account)
        self.create_update_twitter_stream_event()
        return account_id

    def get_twitter_accounts(self) -> List[TwitterAccountEntry]:
        return self.squeak_db.get_twitter_accounts()

    def delete_twitter_account(self, twitter_account_id: int) -> None:
        self.squeak_db.delete_twitter_account(twitter_account_id)
        self.create_update_twitter_stream_event()

    def update_twitter_stream(self) -> None:
        self.tweet_forwarder.start_processing(self)
