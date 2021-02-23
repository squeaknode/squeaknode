import logging

from proto import squeak_admin_pb2
from squeaknode.admin.profile_image_util import bytes_to_base64_string
from squeaknode.admin.profile_image_util import load_default_profile_image
from squeaknode.core.received_offer_with_peer import ReceivedOfferWithPeer
from squeaknode.core.received_payment import ReceivedPayment
from squeaknode.core.received_payment_summary import ReceivedPaymentSummary
from squeaknode.core.sent_offer import SentOffer
from squeaknode.core.sent_payment_summary import SentPaymentSummary
from squeaknode.core.sent_payment_with_peer import SentPaymentWithPeer
from squeaknode.core.squeak_entry_with_profile import SqueakEntryWithProfile
from squeaknode.core.squeak_peer import SqueakPeer
from squeaknode.core.squeak_profile import SqueakProfile
from squeaknode.core.util import get_hash


logger = logging.getLogger(__name__)


DEFAULT_PROFILE_IMAGE = load_default_profile_image()


def squeak_entry_to_message(squeak_entry_with_profile: SqueakEntryWithProfile) -> squeak_admin_pb2.SqueakDisplayEntry:
    squeak_entry = squeak_entry_with_profile.squeak_entry
    squeak = squeak_entry.squeak
    block_header = squeak_entry.block_header
    liked = squeak_entry.liked
    is_unlocked = squeak.HasDecryptionKey()
    content_str = squeak.GetDecryptedContentStr() if is_unlocked else None
    is_reply = squeak.is_reply
    reply_to = squeak.hashReplySqk.hex() if is_reply else None
    author_address = str(squeak.GetAddress())
    squeak_profile = squeak_entry_with_profile.squeak_profile
    is_author_known = False
    profile_msg = None
    if squeak_profile is not None:
        is_author_known = True
        profile_msg = squeak_profile_to_message(squeak_profile)
    return squeak_admin_pb2.SqueakDisplayEntry(
        squeak_hash=get_hash(squeak).hex(),
        is_unlocked=squeak.HasDecryptionKey(),
        content_str=content_str,
        block_height=squeak.nBlockHeight,
        block_hash=squeak.hashBlock.hex(),
        block_time=block_header.nTime,
        is_reply=is_reply,
        reply_to=reply_to,
        author_address=author_address,
        is_author_known=is_author_known,
        author=profile_msg,
        liked=liked,
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
        sharing=squeak_profile.sharing,
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
        host=squeak_peer.address.host,
        port=squeak_peer.address.port,
        uploading=squeak_peer.uploading,
        downloading=squeak_peer.downloading,
    )


def offer_entry_to_message(received_offer_entry: ReceivedOfferWithPeer) -> squeak_admin_pb2.OfferDisplayEntry:
    received_offer = received_offer_entry.received_offer
    if received_offer.received_offer_id is None:
        raise Exception("Received offer id cannot be None.")
    peer = received_offer_entry.peer
    has_peer = False
    peer_msg = None
    if peer is not None:
        has_peer = True
        peer_msg = squeak_peer_to_message(peer)
    return squeak_admin_pb2.OfferDisplayEntry(
        offer_id=received_offer.received_offer_id,
        squeak_hash=received_offer.squeak_hash.hex(),
        price_msat=received_offer.price_msat,
        node_pubkey=received_offer.destination,
        node_host=received_offer.lightning_address.host,
        node_port=received_offer.lightning_address.port,
        has_peer=has_peer,
        peer=peer_msg,
        invoice_timestamp=received_offer.invoice_timestamp,
        invoice_expiry=received_offer.invoice_expiry,
    )


def sent_payment_with_peer_to_message(sent_payment_with_peer: SentPaymentWithPeer) -> squeak_admin_pb2.SentPayment:
    sent_payment = sent_payment_with_peer.sent_payment
    if sent_payment.sent_payment_id is None:
        raise Exception("Sent payment id cannot be None.")
    peer = sent_payment_with_peer.peer
    has_peer = False
    peer_msg = None
    if peer is not None:
        has_peer = True
        peer_msg = squeak_peer_to_message(peer)
    if sent_payment.created is None:
        raise Exception("Sent payment created time not found.")
    return squeak_admin_pb2.SentPayment(
        sent_payment_id=sent_payment.sent_payment_id,
        has_peer=has_peer,
        peer=peer_msg,
        squeak_hash=sent_payment.squeak_hash.hex(),
        payment_hash=sent_payment.payment_hash.hex(),
        price_msat=sent_payment.price_msat,
        node_pubkey=sent_payment.node_pubkey,
        valid=sent_payment.valid,
        time_s=int(sent_payment.created.timestamp()),
    )


def squeak_entry_to_detail_message(squeak_entry_with_profile: SqueakEntryWithProfile) -> squeak_admin_pb2.SqueakDetailEntry:
    squeak_entry = squeak_entry_with_profile.squeak_entry
    squeak = squeak_entry.squeak
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
        client_host=received_payment.client_addr.host,
        client_port=received_payment.client_addr.port,
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
