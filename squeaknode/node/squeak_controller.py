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
from typing import Union

import sqlalchemy
import squeak.params
from squeak.core import CSqueak
from squeak.core.signing import CSigningKey
from squeak.core.signing import CSqueakAddress
from squeak.messages import msg_getdata
from squeak.messages import msg_getsqueaks
from squeak.messages import msg_subscribe
from squeak.messages import MsgSerializable
from squeak.net import CInterested
from squeak.net import CInv
from squeak.net import CSqueakLocator

from squeaknode.core.block_range import BlockRange
from squeaknode.core.offer import Offer
from squeaknode.core.peer_address import PeerAddress
from squeaknode.core.received_offer import ReceivedOffer
from squeaknode.core.received_payment_summary import ReceivedPaymentSummary
from squeaknode.core.sent_offer import SentOffer
from squeaknode.core.sent_payment import SentPayment
from squeaknode.core.sent_payment_summary import SentPaymentSummary
from squeaknode.core.squeak_entry import SqueakEntry
from squeaknode.core.squeak_peer import SqueakPeer
from squeaknode.core.squeak_profile import SqueakProfile
from squeaknode.core.util import get_hash
from squeaknode.core.util import is_address_valid
from squeaknode.core.util import squeak_matches_interest
from squeaknode.network.peer import Peer
from squeaknode.node.listener_subscription_client import EventListener
from squeaknode.node.received_payments_subscription_client import ReceivedPaymentsSubscriptionClient
from squeaknode.node.temporary_interest_manager import TemporaryInterest
from squeaknode.node.temporary_interest_manager import TemporaryInterestManager


logger = logging.getLogger(__name__)


class SqueakController:

    def __init__(
        self,
        squeak_db,
        squeak_core,
        payment_processor,
        network_manager,
        config,
    ):
        self.squeak_db = squeak_db
        self.squeak_core = squeak_core
        self.payment_processor = payment_processor
        self.network_manager = network_manager
        self.new_squeak_listener = EventListener()
        self.new_received_offer_listener = EventListener()
        self.new_secret_key_listener = EventListener()
        self.temporary_interest_manager = TemporaryInterestManager()
        self.config = config

    def save_squeak(self, squeak: CSqueak) -> bytes:
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

    def make_squeak(self, profile_id: int, content_str: str, replyto_hash: bytes) -> bytes:
        squeak_profile = self.squeak_db.get_profile(profile_id)
        squeak, decryption_key = self.squeak_core.make_squeak(
            squeak_profile, content_str, replyto_hash)
        inserted_squeak_hash = self.save_squeak(squeak)
        self.unlock_squeak(
            inserted_squeak_hash,
            decryption_key,
        )
        return inserted_squeak_hash

    def get_squeak(self, squeak_hash: bytes) -> Optional[CSqueak]:
        return self.squeak_db.get_squeak(squeak_hash)

    def get_squeak_secret_key(self, squeak_hash: bytes) -> Optional[bytes]:
        return self.squeak_db.get_squeak_secret_key(squeak_hash)

    def delete_squeak(self, squeak_hash: bytes) -> None:
        num_deleted_offers = self.squeak_db.delete_offers_for_squeak(
            squeak_hash)
        logger.info("Deleted number of offers : {}".format(num_deleted_offers))
        self.squeak_db.delete_squeak(squeak_hash)

    def save_received_squeak(self, squeak: CSqueak) -> None:
        saved_squeak_hash = None
        counter = self.get_temporary_interest_counter(squeak)
        if counter:
            saved_squeak_hash = self.save_squeak(squeak)
            counter.increment()
        elif self.squeak_matches_interest(squeak):
            saved_squeak_hash = self.save_squeak(squeak)
        # Download offers for the new squeak
        if saved_squeak_hash:
            self.download_offers(saved_squeak_hash)

    def squeak_matches_interest(self, squeak: CSqueak) -> bool:
        locator = self.get_interested_locator()
        for interest in locator.vInterested:
            if squeak_matches_interest(squeak, interest) \
               and self.squeak_in_limit_of_interest(squeak, interest):
                return True
        return False

    def squeak_in_limit_of_interest(self, squeak: CSqueak, interest: CInterested) -> bool:
        return self.squeak_db.number_of_squeaks_with_address_in_block_range(
            str(squeak.GetAddress),
            interest.nMinBlockHeight,
            interest.nMaxBlockHeight,
        ) < self.config.node.max_squeaks_per_address_in_block_range

    def get_temporary_interest_counter(self, squeak: CSqueak) -> Optional[TemporaryInterest]:
        return self.temporary_interest_manager.lookup_counter(squeak)

    def get_offer_or_secret_key(self, squeak_hash: bytes, peer_address: PeerAddress) -> Optional[Union[bytes, Offer]]:
        squeak = self.get_squeak(squeak_hash)
        if squeak is None:
            return None
        price = self.get_price_for_squeak(squeak)
        if price == 0:
            return self.get_squeak_secret_key(squeak_hash)
        else:
            return self.get_offer(
                squeak_hash=squeak_hash,
                peer_address=peer_address,
            )

    def get_offer(self, squeak_hash: bytes, peer_address: PeerAddress) -> Optional[Offer]:
        sent_offer = self.get_sent_offer_for_peer(squeak_hash, peer_address)
        if sent_offer is None:
            return None
        return self.squeak_core.package_offer(
            sent_offer,
            self.config.lnd.external_host,
            self.config.lnd.port,
        )

    def get_sent_offer_for_peer(self, squeak_hash: bytes, peer_address: PeerAddress) -> Optional[SentOffer]:
        # Check if there is an existing offer for the hash/peer_address combination
        sent_offer = self.squeak_db.get_sent_offer_by_squeak_hash_and_peer(
            squeak_hash,
            peer_address,
        )
        if sent_offer:
            return sent_offer
        squeak = self.get_squeak(squeak_hash)
        secret_key = self.get_squeak_secret_key(squeak_hash)
        if squeak is None or secret_key is None:
            return None
        sent_offer = self.squeak_core.create_offer(
            squeak,
            secret_key,
            peer_address,
            self.config.node.price_msat,
        )
        self.squeak_db.insert_sent_offer(sent_offer)
        return sent_offer

    def get_price_for_squeak(self, squeak: CSqueak) -> int:
        squeak_address = str(squeak.GetAddress())
        logger.info(
            "Looking for profile with address: {}".format(squeak_address))
        squeak_profile = self.get_squeak_profile_by_address(squeak_address)
        logger.info(
            "Checking price for squeak with profile: {}".format(squeak_profile))
        if squeak_profile is not None and squeak_profile.use_custom_price:
            return squeak_profile.custom_price_msat
        return self.config.node.price_msat

    def create_signing_profile(self, profile_name: str) -> int:
        if len(profile_name) == 0:
            raise Exception(
                "Profile name cannot be empty.",
            )
        signing_key = CSigningKey.generate()
        verifying_key = signing_key.get_verifying_key()
        address = CSqueakAddress.from_verifying_key(verifying_key)
        signing_key_str = str(signing_key)
        signing_key_bytes = signing_key_str.encode()
        squeak_profile = SqueakProfile(
            profile_name=profile_name,
            private_key=signing_key_bytes,
            address=str(address),
        )
        profile_id = self.squeak_db.insert_profile(squeak_profile)
        self.update_subscriptions()
        return profile_id

    def import_signing_profile(self, profile_name: str, private_key: str) -> int:
        signing_key = CSigningKey(private_key)
        verifying_key = signing_key.get_verifying_key()
        address = CSqueakAddress.from_verifying_key(verifying_key)
        signing_key_str = str(signing_key)
        signing_key_bytes = signing_key_str.encode()
        squeak_profile = SqueakProfile(
            profile_name=profile_name,
            private_key=signing_key_bytes,
            address=str(address),
        )
        profile_id = self.squeak_db.insert_profile(squeak_profile)
        self.update_subscriptions()
        return profile_id

    def create_contact_profile(self, profile_name: str, squeak_address: str) -> int:
        if len(profile_name) == 0:
            raise Exception(
                "Profile name cannot be empty.",
            )
        if not is_address_valid(squeak_address):
            raise Exception(
                "Invalid squeak address: {}".format(
                    squeak_address
                ),
            )
        squeak_profile = SqueakProfile(
            profile_name=profile_name,
            address=squeak_address,
        )
        profile_id = self.squeak_db.insert_profile(squeak_profile)
        self.update_subscriptions()
        return profile_id

    def get_profiles(self) -> List[SqueakProfile]:
        return self.squeak_db.get_profiles()

    def get_signing_profiles(self) -> List[SqueakProfile]:
        return self.squeak_db.get_signing_profiles()

    def get_contact_profiles(self) -> List[SqueakProfile]:
        return self.squeak_db.get_contact_profiles()

    def get_squeak_profile(self, profile_id: int) -> Optional[SqueakProfile]:
        return self.squeak_db.get_profile(profile_id)

    def get_squeak_profile_by_address(self, address: str) -> Optional[SqueakProfile]:
        return self.squeak_db.get_profile_by_address(address)

    def get_squeak_profile_by_name(self, name: str) -> Optional[SqueakProfile]:
        return self.squeak_db.get_profile_by_name(name)

    def set_squeak_profile_following(self, profile_id: int, following: bool) -> None:
        self.squeak_db.set_profile_following(profile_id, following)
        self.update_subscriptions()

    def set_squeak_profile_use_custom_price(self, profile_id: int, use_custom_price: bool) -> None:
        self.squeak_db.set_profile_use_custom_price(
            profile_id, use_custom_price)

    def rename_squeak_profile(self, profile_id: int, profile_name: str) -> None:
        self.squeak_db.set_profile_name(profile_id, profile_name)

    def delete_squeak_profile(self, profile_id: int) -> None:
        self.squeak_db.delete_profile(profile_id)
        self.update_subscriptions()

    def set_squeak_profile_image(self, profile_id: int, profile_image: bytes) -> None:
        self.squeak_db.set_profile_image(profile_id, profile_image)

    def clear_squeak_profile_image(self, profile_id: int) -> None:
        self.squeak_db.set_profile_image(profile_id, None)

    def get_squeak_profile_private_key(self, profile_id: int) -> bytes:
        profile = self.get_squeak_profile(profile_id)
        if profile is None:
            raise Exception("Profile with id: {} does not exist.".format(
                profile_id
            ))
        if profile.private_key is None:
            raise Exception("Profile with id: {} does not have a private key.".format(
                profile_id
            ))
        return profile.private_key

    def create_peer(self, peer_name: str, peer_address: PeerAddress):
        if len(peer_name) == 0:
            raise Exception(
                "Peer name cannot be empty.",
            )
        port = peer_address.port or squeak.params.params.DEFAULT_PORT
        peer_address = PeerAddress(
            host=peer_address.host,
            port=port,
        )
        squeak_peer = SqueakPeer(
            peer_id=None,
            peer_name=peer_name,
            address=peer_address,
            autoconnect=False,
        )
        return self.squeak_db.insert_peer(squeak_peer)

    def get_peer(self, peer_id: int) -> Optional[SqueakPeer]:
        return self.squeak_db.get_peer(peer_id)

    def get_peers(self):
        return self.squeak_db.get_peers()

    def get_autoconnect_peers(self) -> List[SqueakPeer]:
        return self.squeak_db.get_autoconnect_peers()

    def set_peer_autoconnect(self, peer_id: int, autoconnect: bool):
        self.squeak_db.set_peer_autoconnect(peer_id, autoconnect)

    def rename_peer(self, peer_id: int, peer_name: str):
        self.squeak_db.set_peer_name(peer_id, peer_name)

    def delete_peer(self, peer_id: int):
        self.squeak_db.delete_peer(peer_id)

    def get_received_offers(self, squeak_hash: bytes) -> List[ReceivedOffer]:
        return self.squeak_db.get_received_offers(squeak_hash)

    def get_received_offer_for_squeak_and_peer(
            self,
            squeak_hash: bytes,
            peer_addresss: PeerAddress,
    ) -> Optional[ReceivedOffer]:
        return self.squeak_db.get_received_offer_for_squeak_and_peer(
            squeak_hash,
            peer_addresss,
        )

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

    def get_sent_payments(self) -> List[SentPayment]:
        return self.squeak_db.get_sent_payments()

    def get_sent_payment(self, sent_payment_id: int) -> Optional[SentPayment]:
        return self.squeak_db.get_sent_payment(sent_payment_id)

    def get_sent_offers(self):
        return self.squeak_db.get_sent_offers()

    def get_received_payments(self):
        return self.squeak_db.get_received_payments()

    def delete_all_expired_received_offers(self):
        num_expired_received_offers = self.squeak_db.delete_expired_received_offers()
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

    def get_squeak_entries_for_address(
            self,
            address: str,
            limit: int,
            last_entry: Optional[SqueakEntry],
    ) -> List[SqueakEntry]:
        return self.squeak_db.get_squeak_entries_for_address(
            address,
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

    def save_received_offer(self, offer: Offer, peer_address: PeerAddress) -> None:
        logger.info("Saving received offer: {}".format(offer))
        squeak = self.get_squeak(offer.squeak_hash)
        secret_key = self.get_squeak_secret_key(offer.squeak_hash)
        if squeak is None or secret_key is not None:
            return
        received_offer = self.squeak_core.unpack_offer(
            squeak,
            offer,
            peer_address,
        )
        try:
            offer_id = self.squeak_db.insert_received_offer(received_offer)
            received_offer = received_offer._replace(
                received_offer_id=offer_id)
            self.new_received_offer_listener.handle_new_item(received_offer)
        except sqlalchemy.exc.IntegrityError:
            logger.debug("Failed to save duplicate offer.")

    def get_followed_addresses(self) -> List[str]:
        followed_profiles = self.squeak_db.get_following_profiles()
        return [profile.address for profile in followed_profiles]

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
        self.network_manager.connect_peer(peer_address)

    def connect_saved_peers(self) -> None:
        peers = self.get_autoconnect_peers()
        for peer in peers:
            self.network_manager.connect_peer(
                peer.address,
            )

    def get_connected_peer(self, peer_address: PeerAddress):
        return self.network_manager.get_connected_peer(peer_address)

    def get_connected_peers(self) -> List[Peer]:
        return self.network_manager.get_connected_peers()

    def lookup_squeaks(
            self,
            addresses: List[str],
            min_block: int,
            max_block: int,
            reply_to_hash: bytes,
    ) -> List[bytes]:
        return self.squeak_db.lookup_squeaks(
            addresses,
            min_block,
            max_block,
            reply_to_hash,
            include_locked=True,
        )

    def lookup_secret_keys(
            self,
            addresses: List[str],
            min_block: int,
            max_block: int,
            reply_to_hash: bytes,
    ) -> List[bytes]:
        return self.squeak_db.lookup_squeaks(
            addresses,
            min_block,
            max_block,
            reply_to_hash,
        )

    def get_interested_locator(self):
        block_range = self.get_block_range()
        followed_addresses = self.get_followed_addresses()
        if len(followed_addresses) == 0:
            return CSqueakLocator(
                vInterested=[],
            )
        interests = [
            CInterested(
                addresses=[CSqueakAddress(address)
                           for address in followed_addresses],
                nMinBlockHeight=block_range.min_block,
                nMaxBlockHeight=block_range.max_block,
            )
        ]
        return CSqueakLocator(
            vInterested=interests,
        )

    def download_squeaks(
            self,
            addresses: List[str],
            min_block: int,
            max_block: int,
            replyto_hash: Optional[bytes],
    ):
        interest = CInterested(
            addresses=[CSqueakAddress(address)
                       for address in addresses],
            nMinBlockHeight=min_block,
            nMaxBlockHeight=max_block,
            replyto_squeak_hash=replyto_hash,
        ) if replyto_hash else CInterested(
            addresses=[CSqueakAddress(address)
                       for address in addresses],
            nMinBlockHeight=min_block,
            nMaxBlockHeight=max_block,
        )
        self.temporary_interest_manager.add_range_interest(10, interest)
        locator = CSqueakLocator(
            vInterested=[interest],
        )
        getsqueaks_msg = msg_getsqueaks(
            locator=locator,
        )
        self.broadcast_msg(getsqueaks_msg)

    def download_single_squeak(self, squeak_hash: bytes):
        logger.info("Downloading single squeak: {}".format(
            squeak_hash.hex(),
        ))
        # Add the temporary interest in this hash.
        self.temporary_interest_manager.add_hash_interest(1, squeak_hash)
        invs = [
            CInv(type=1, hash=squeak_hash)
        ]
        getdata_msg = msg_getdata(
            inv=invs,
        )
        self.broadcast_msg(getdata_msg)

    def download_offers(self, squeak_hash: bytes):
        logger.info("Downloading offers for squeak: {}".format(
            squeak_hash.hex(),
        ))
        invs = [
            CInv(type=2, hash=squeak_hash)
        ]
        getdata_msg = msg_getdata(inv=invs)
        self.broadcast_msg(getdata_msg)

    def download_replies(self, squeak_hash: bytes):
        logger.info("Downloading replies for squeak: {}".format(
            squeak_hash.hex(),
        ))
        interest = CInterested(
            hashReplySqk=squeak_hash,
        )
        self.temporary_interest_manager.add_range_interest(10, interest)
        locator = CSqueakLocator(
            vInterested=[interest],
        )
        getsqueaks_msg = msg_getsqueaks(
            locator=locator,
        )
        self.broadcast_msg(getsqueaks_msg)

    def download_address_squeaks(self, squeak_address: str):
        logger.info("Downloading address squeaks for address: {}".format(
            squeak_address,
        ))
        interest = CInterested(
            addresses=[CSqueakAddress(squeak_address)],
        )
        self.temporary_interest_manager.add_range_interest(10, interest)
        locator = CSqueakLocator(
            vInterested=[interest],
        )
        getsqueaks_msg = msg_getsqueaks(
            locator=locator,
        )
        self.broadcast_msg(getsqueaks_msg)

    def broadcast_msg(self, msg: MsgSerializable) -> None:
        self.network_manager.broadcast_msg(msg)

    def disconnect_peer(self, peer_address: PeerAddress) -> None:
        logger.info("Disconnect to peer: {}".format(
            peer_address,
        ))
        self.network_manager.disconnect_peer(peer_address)

    def subscribe_connected_peers(self, stopped: threading.Event):
        return self.network_manager.subscribe_connected_peers(stopped)

    def subscribe_connected_peer(self, peer_address: PeerAddress, stopped: threading.Event):
        return self.network_manager.subscribe_connected_peer(peer_address, stopped)

    def subscribe_new_squeaks(self, stopped: threading.Event):
        yield from self.new_squeak_listener.yield_items(stopped)

    def subscribe_new_secret_keys(self, stopped: threading.Event):
        yield from self.new_secret_key_listener.yield_items(stopped)

    def update_subscriptions(self):
        locator = self.get_interested_locator()
        subscribe_msg = msg_subscribe(
            locator=locator,
        )
        self.broadcast_msg(subscribe_msg)

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

    def subscribe_squeak_address_entries(self, squeak_address: str, stopped: threading.Event):
        for item in self.new_squeak_listener.yield_items(stopped):
            if squeak_address == str(item.GetAddress()):
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
            followed_addresses = self.get_followed_addresses()
            if str(item.GetAddress()) in set(followed_addresses):
                squeak_hash = get_hash(item)
                yield self.get_squeak_entry(squeak_hash)
