import logging
import threading
from typing import List
from typing import Optional

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
from squeaknode.core.squeak_entry_with_profile import SqueakEntryWithProfile
from squeaknode.core.squeak_peer import SqueakPeer
from squeaknode.core.squeak_profile import SqueakProfile
from squeaknode.core.util import get_hash
from squeaknode.core.util import is_address_valid
from squeaknode.node.new_squeak_listener import NewSqueakListener
from squeaknode.node.new_squeak_listener import NewSqueakSubscriptionClient
from squeaknode.node.received_payments_subscription_client import ReceivedPaymentsSubscriptionClient


logger = logging.getLogger(__name__)


class SqueakController:

    def __init__(
        self,
        squeak_db,
        squeak_core,
        squeak_rate_limiter,
        payment_processor,
        network_manager,
        config,
    ):
        self.squeak_db = squeak_db
        self.squeak_core = squeak_core
        self.squeak_rate_limiter = squeak_rate_limiter
        self.payment_processor = payment_processor
        self.network_manager = network_manager
        self.new_squeak_listener = NewSqueakListener()
        self.config = config

    def save_squeak(self, squeak: CSqueak) -> bytes:
        """Saves a squeak.

        Args:
            squeak: The squeak to be validated.

        Returns:
            bytes: the squeak hash.

        Raises:
            Exception: If squeak fails to save.
        """
        # Get the block header for the squeak.
        block_header = self.squeak_core.get_block_header(squeak)
        squeak_entry = SqueakEntry(
            squeak=squeak,
            block_header=block_header,
        )

        # Check if limit exceeded.
        if self.get_number_of_squeaks() >= self.config.core.max_squeaks:
            raise Exception("Exceeded max number of squeaks.")
        # Insert the squeak in db.
        inserted_squeak_hash = self.squeak_db.insert_squeak(
            squeak, squeak_entry.block_header)
        logger.info("Saved squeak: {}".format(
            inserted_squeak_hash.hex(),
        ))
        self.new_squeak_listener.handle_new_squeak(squeak)
        return inserted_squeak_hash

    def unlock_squeak(self, squeak_hash: bytes, secret_key: bytes):
        squeak_entry = self.squeak_db.get_squeak_entry(squeak_hash)
        squeak = squeak_entry.squeak
        decrypted_content = self.squeak_core.get_decrypted_content(
            squeak,
            secret_key,
        )
        # TODO: set decryption key should also take decrypted content.
        self.squeak_db.set_squeak_decryption_key(
            squeak_hash,
            secret_key,
        )
        logger.info("Unlocked squeak: {} with content: {}".format(
            squeak_hash.hex(),
            decrypted_content,
        ))

    def make_squeak(self, profile_id: int, content_str: str, replyto_hash: bytes) -> bytes:
        squeak_profile = self.squeak_db.get_profile(profile_id)
        squeak = self.squeak_core.make_squeak(
            squeak_profile, content_str, replyto_hash)
        decryption_key = squeak.GetDecryptionKey()
        inserted_squeak_hash = self.save_squeak(squeak)
        self.unlock_squeak(
            inserted_squeak_hash,
            decryption_key,
        )
        return inserted_squeak_hash

    def get_squeak(self, squeak_hash: bytes) -> Optional[CSqueak]:
        squeak_entry = self.squeak_db.get_squeak_entry(squeak_hash)
        if squeak_entry is None:
            return None
        return squeak_entry.squeak

    def delete_squeak(self, squeak_hash: bytes) -> None:
        num_deleted_offers = self.squeak_db.delete_offers_for_squeak(
            squeak_hash)
        logger.info("Deleted number of offers : {}".format(num_deleted_offers))
        self.squeak_db.delete_squeak(squeak_hash)

    def get_buy_offer(self, squeak_hash: bytes, peer_address: PeerAddress) -> Offer:
        # Check if there is an existing offer for the hash/peer_address combination
        sent_offer = self.get_saved_sent_offer(squeak_hash, peer_address)
        return self.squeak_core.package_offer(
            sent_offer,
            self.config.lnd.external_host,
            self.config.lnd.port,
        )

    def get_saved_sent_offer(self, squeak_hash: bytes, peer_address: PeerAddress) -> SentOffer:
        # Check if there is an existing offer for the hash/peer_address combination
        sent_offer = self.squeak_db.get_sent_offer_by_squeak_hash_and_peer(
            squeak_hash,
            peer_address,
        )
        if sent_offer:
            return sent_offer
        squeak = self.get_squeak(squeak_hash)
        sent_offer = self.squeak_core.create_offer(
            squeak,
            peer_address,
            self.config.core.price_msat,
        )
        self.squeak_db.insert_sent_offer(sent_offer)
        return sent_offer

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
            profile_id=None,
            profile_name=profile_name,
            private_key=signing_key_bytes,
            address=str(address),
            following=True,
            profile_image=None,
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
            profile_id=None,
            profile_name=profile_name,
            private_key=signing_key_bytes,
            address=str(address),
            following=True,
            profile_image=None,
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
            profile_id=None,
            profile_name=profile_name,
            private_key=None,
            address=squeak_address,
            following=True,
            profile_image=None,
        )
        profile_id = self.squeak_db.insert_profile(squeak_profile)
        self.update_subscriptions()
        return profile_id

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
        sent_offer_retention_s = self.config.core.sent_offer_retention_s
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
            for payment in client.get_received_payments():
                yield payment

    def get_block_range(self) -> BlockRange:
        max_block = self.squeak_core.get_best_block_height()
        block_interval = self.config.core.interest_block_interval
        min_block = max(0, max_block - block_interval)
        return BlockRange(min_block, max_block)

    def get_network(self) -> str:
        return self.config.core.network

    # TODO: Rename this method. All it does is unpack.
    def get_offer(self, squeak: CSqueak, offer: Offer, peer_address: PeerAddress) -> ReceivedOffer:
        return self.squeak_core.unpack_offer(squeak, offer, peer_address)

    def get_squeak_entry_with_profile(self, squeak_hash: bytes) -> Optional[SqueakEntryWithProfile]:
        return self.squeak_db.get_squeak_entry_with_profile(squeak_hash)

    def get_timeline_squeak_entries_with_profile(self):
        return self.squeak_db.get_timeline_squeak_entries_with_profile()

    def get_liked_squeak_entries_with_profile(self):
        return self.squeak_db.get_liked_squeak_entries_with_profile()

    def get_squeak_entries_with_profile_for_address(
        self, address: str, min_block: int, max_block: int
    ):
        return self.squeak_db.get_squeak_entries_with_profile_for_address(
            address,
            min_block,
            max_block,
        )

    def get_ancestor_squeak_entries_with_profile(self, squeak_hash: bytes):
        return self.squeak_db.get_thread_ancestor_squeak_entries_with_profile(
            squeak_hash,
        )

    def get_reply_squeak_entries_with_profile(self, squeak_hash: bytes):
        return self.squeak_db.get_thread_reply_squeak_entries_with_profile(
            squeak_hash,
        )

    def lookup_squeaks(self, addresses: List[str], min_block: int, max_block: int):
        return self.squeak_db.lookup_squeaks(
            addresses,
            min_block,
            max_block,
        )

    def get_number_of_squeaks(self) -> int:
        return self.squeak_db.get_number_of_squeaks()

    def save_offer(self, received_offer: ReceivedOffer) -> None:
        logger.info("Saving received offer: {}".format(received_offer))
        try:
            self.squeak_db.insert_received_offer(received_offer)
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
            self.config.core.squeak_retention_s,
        )
        for squeak_entry_with_profile in squeaks_to_delete:
            squeak = squeak_entry_with_profile.squeak_entry.squeak
            squeak_hash = get_hash(squeak)
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

    def get_address(self):
        return self.network_manager.get_address()

    def get_remote_address(self, address):
        return self.network_manager.get_remote_address(address)

    def get_connected_peer(self, peer_address: PeerAddress):
        return self.network_manager.get_connected_peer(peer_address)

    def get_connected_peers(self):
        return self.network_manager.get_connected_peers()

    def lookup_squeaks_for_interest(
            self,
            address: str,
            min_block: int,
            max_block: int,
            reply_to_hash: bytes,
    ):
        return self.squeak_db.lookup_squeaks(
            address,
            min_block,
            max_block,
            reply_to_hash,
        )

    def filter_known_invs(self, invs):
        ret = []
        for inv in invs:
            if inv.type == 1:
                squeak_entry = self.squeak_db.get_squeak_entry(
                    inv.hash,
                )
                if squeak_entry is None:
                    ret.append(
                        CInv(type=1, hash=inv.hash)
                    )
                # TODO: Decide if offers should be loaded whenever missing?
                # elif not squeak_entry.squeak.HasDecryptionKey():
                #     ret.append(
                #         CInv(type=2, hash=inv.hash)
                #     )
        return ret

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

    def download_squeaks(self):
        locator = self.get_interested_locator()
        getsqueaks_msg = msg_getsqueaks(
            locator=locator,
        )
        self.broadcast_msg(getsqueaks_msg)

    def download_single_squeak(self, squeak_hash: bytes):
        logger.info("Downloading single squeak: {}".format(
            squeak_hash.hex(),
        ))
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
        interests = [
            CInterested(
                hashReplySqk=squeak_hash,
            )
        ]
        locator = CSqueakLocator(
            vInterested=interests,
        )
        getsqueaks_msg = msg_getsqueaks(
            locator=locator,
        )
        self.broadcast_msg(getsqueaks_msg)

    # def filter_shared_squeak_locator(self, interests: List[CInterested]):
    #     ret = []
    #     block_range = self.get_block_range()
    #     followed_addresses = self.get_followed_addresses()
    #     for interest in interests:
    #         if str(interest.address) in followed_addresses:
    #             min_block = max(interest.nMinBlockHeight,
    #                             block_range.min_block)
    #             max_block = min(interest.nMaxBlockHeight,
    #                             block_range.max_block)
    #             if min_block <= max_block:
    #                 ret.append(
    #                     CInterested(
    #                         address=interest.address,
    #                         nMinBlockHeight=min_block,
    #                         nMaxBlockHeight=max_block,
    #                     )
    #                 )
    #     return ret

    def broadcast_msg(self, msg: MsgSerializable) -> None:
        self.network_manager.broadcast_msg(msg)

    def disconnect_peer(self, peer_address: PeerAddress) -> None:
        logger.info("Disconnect to peer: {}".format(
            peer_address,
        ))
        self.network_manager.disconnect_peer(peer_address)

    def subscribe_connected_peers(self, stopped: threading.Event):
        # with ReceivedPaymentsSubscriptionClient(
        #     self.squeak_db,
        #     initial_index,
        #     stopped,
        # ).open_subscription() as client:
        #     for payment in client.get_received_payments():
        #         yield payment
        return self.network_manager.subscribe_connected_peers(stopped)

    def subscribe_new_squeaks(self, stopped: threading.Event):
        subscription_client = NewSqueakSubscriptionClient(
            self.new_squeak_listener,
            stopped,
        )
        with subscription_client.open_subscription():
            for result in subscription_client.get_squeak():
                yield result

    def update_subscriptions(self):
        locator = self.get_interested_locator()
        for peer in self.network_manager.get_connected_peers():
            subscribe_msg = msg_subscribe(
                locator=locator,
            )
            peer.send_msg(subscribe_msg)
