import logging

from squeak.core import CSqueak

from proto import squeak_admin_pb2
from squeaknode.admin.profile_image_util import bytes_to_base64_string
from squeaknode.admin.profile_image_util import load_default_profile_image
from squeaknode.core.peer_address import PeerAddress
from squeaknode.core.received_offer import ReceivedOffer
from squeaknode.core.received_payment import ReceivedPayment
from squeaknode.core.received_payment_summary import ReceivedPaymentSummary
from squeaknode.core.sent_offer import SentOffer
from squeaknode.core.sent_payment import SentPayment
from squeaknode.core.sent_payment_summary import SentPaymentSummary
from squeaknode.core.squeak_entry_with_profile import SqueakEntryWithProfile
from squeaknode.core.squeak_peer import SqueakPeer
from squeaknode.core.squeak_profile import SqueakProfile
from squeaknode.network.peer import Peer

logger = logging.getLogger(__name__)


DEFAULT_PROFILE_IMAGE = load_default_profile_image()

#  TODO: Remove this after reply is nullable column
# EMPTY_HASH = b'\x00' * 32


def squeak_entry_to_message(squeak_entry_with_profile: SqueakEntryWithProfile) -> squeak_admin_pb2.SqueakDisplayEntry:
    squeak_entry = squeak_entry_with_profile.squeak_entry
    squeak_profile = squeak_entry_with_profile.squeak_profile
    is_reply = bool(squeak_entry.reply_to)
    reply_to = squeak_entry.reply_to.hex() if squeak_entry.reply_to else None
    is_author_known = False
    profile_msg = None
    if squeak_profile is not None:
        is_author_known = True
        profile_msg = squeak_profile_to_message(squeak_profile)
    return squeak_admin_pb2.SqueakDisplayEntry(
        squeak_hash=squeak_entry.squeak_hash.hex(),
        is_unlocked=squeak_entry.is_unlocked,
        content_str=squeak_entry.content,  # type: ignore
        block_height=squeak_entry.block_height,
        block_hash=squeak_entry.block_hash.hex(),
        block_time=squeak_entry.block_time,
        is_reply=is_reply,
        reply_to=reply_to,  # type: ignore
        author_address=squeak_entry.address,
        is_author_known=is_author_known,
        author=profile_msg,
        liked_time_s=squeak_entry.liked_time,  # type: ignore
    )


def squeak_profile_to_message(squeak_profile: SqueakProfile) -> squeak_admin_pb2.SqueakProfile:
    if squeak_profile.profile_id is None:
        raise Exception("Profile id cannot be None.")
    has_private_key = squeak_profile.private_key is not None
    profile_image = squeak_profile.profile_image or DEFAULT_PROFILE_IMAGE
    has_custom_profile_image = squeak_profile.profile_image is not None
    image_base64_str = bytes_to_base64_string(profile_image)
    return squeak_admin_pb2.SqueakProfile(
        profile_id=squeak_profile.profile_id,
        profile_name=squeak_profile.profile_name,
        has_private_key=has_private_key,
        address=squeak_profile.address,
        following=squeak_profile.following,
        profile_image=image_base64_str,
        has_custom_profile_image=has_custom_profile_image,
    )


def squeak_peer_to_message(squeak_peer: SqueakPeer) -> squeak_admin_pb2.SqueakPeer:
    if squeak_peer.peer_id is None:
        raise Exception("Peer id cannot be None.")
    return squeak_admin_pb2.SqueakPeer(
        peer_id=squeak_peer.peer_id,
        peer_name=squeak_peer.peer_name,
        peer_address=peer_address_to_message(squeak_peer.address),
        autoconnect=squeak_peer.autoconnect,
    )


def offer_entry_to_message(received_offer: ReceivedOffer) -> squeak_admin_pb2.OfferDisplayEntry:
    if received_offer.received_offer_id is None:
        raise Exception("Received offer id cannot be None.")
    return squeak_admin_pb2.OfferDisplayEntry(
        offer_id=received_offer.received_offer_id,
        squeak_hash=received_offer.squeak_hash.hex(),
        price_msat=received_offer.price_msat,
        node_pubkey=received_offer.destination,
        node_host=received_offer.lightning_address.host,
        node_port=received_offer.lightning_address.port,
        invoice_timestamp=received_offer.invoice_timestamp,
        invoice_expiry=received_offer.invoice_expiry,
        peer_address=peer_address_to_message(received_offer.peer_address)
    )


def sent_payment_to_message(sent_payment: SentPayment) -> squeak_admin_pb2.SentPayment:
    if sent_payment.sent_payment_id is None:
        raise Exception("Sent payment id cannot be None.")
    if sent_payment.created is None:
        raise Exception("Sent payment created time not found.")
    return squeak_admin_pb2.SentPayment(
        sent_payment_id=sent_payment.sent_payment_id,
        squeak_hash=sent_payment.squeak_hash.hex(),
        payment_hash=sent_payment.payment_hash.hex(),
        price_msat=sent_payment.price_msat,
        node_pubkey=sent_payment.node_pubkey,
        valid=sent_payment.valid,
        time_s=int(sent_payment.created.timestamp()),
        peer_address=peer_address_to_message(sent_payment.peer_address)
    )


def squeak_to_detail_message(squeak: CSqueak) -> squeak_admin_pb2.SqueakDetailEntry:
    serialized_squeak = squeak.serialize()
    return squeak_admin_pb2.SqueakDetailEntry(
        serialized_squeak_hex=serialized_squeak.hex(),
    )


def sent_offer_to_message(sent_offer: SentOffer) -> squeak_admin_pb2.SentOffer:
    if sent_offer.sent_offer_id is None:
        raise Exception("Sent offer id cannot be None.")
    return squeak_admin_pb2.SentOffer(
        sent_offer_id=sent_offer.sent_offer_id,
        squeak_hash=sent_offer.squeak_hash.hex(),
        payment_hash=sent_offer.payment_hash.hex(),
        price_msat=sent_offer.price_msat,
    )


def received_payments_to_message(received_payment: ReceivedPayment) -> squeak_admin_pb2.ReceivedPayment:
    if received_payment.received_payment_id is None:
        raise Exception("Received payment id cannot be None.")
    if received_payment.created is None:
        raise Exception("Received payment created time not found.")
    return squeak_admin_pb2.ReceivedPayment(
        received_payment_id=received_payment.received_payment_id,
        squeak_hash=received_payment.squeak_hash.hex(),
        payment_hash=received_payment.payment_hash.hex(),
        price_msat=received_payment.price_msat,
        time_s=int(received_payment.created.timestamp()),
        peer_address=peer_address_to_message(received_payment.peer_address)
    )


def payment_summary_to_message(
        received_payment_summary: ReceivedPaymentSummary,
        sent_payment_summary: SentPaymentSummary,
) -> squeak_admin_pb2.PaymentSummary:
    return squeak_admin_pb2.PaymentSummary(
        num_received_payments=received_payment_summary.num_received_payments,
        num_sent_payments=sent_payment_summary.num_sent_payments,
        amount_earned_msat=received_payment_summary.total_amount_received_msat,
        amount_spent_msat=sent_payment_summary.total_amount_sent_msat,
    )


def connected_peer_to_message(connected_peer: Peer) -> squeak_admin_pb2.ConnectedPeer:
    return squeak_admin_pb2.ConnectedPeer(
        peer_address=peer_address_to_message(connected_peer.remote_address),
        connect_time_s=connected_peer.connect_time,
    )


def peer_address_to_message(peer_address: PeerAddress) -> squeak_admin_pb2.PeerAddress:
    return squeak_admin_pb2.PeerAddress(
        host=peer_address.host,
        port=peer_address.port,
    )


def message_to_peer_address(peer_address: squeak_admin_pb2.PeerAddress) -> PeerAddress:
    return PeerAddress(
        host=peer_address.host,
        port=peer_address.port,
    )
