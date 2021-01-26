import logging

from proto import squeak_admin_pb2
from squeaknode.core.received_offer_with_peer import ReceivedOfferWithPeer
from squeaknode.core.received_payment_summary import ReceivedPaymentSummary
from squeaknode.core.sent_payment_summary import SentPaymentSummary
from squeaknode.core.squeak_entry_with_profile import SqueakEntryWithProfile
from squeaknode.core.util import get_hash

logger = logging.getLogger(__name__)


def squeak_entry_to_message(squeak_entry_with_profile: SqueakEntryWithProfile):
    if squeak_entry_with_profile is None:
        return None
    squeak_entry = squeak_entry_with_profile.squeak_entry
    squeak = squeak_entry.squeak
    block_header = squeak_entry.block_header
    is_unlocked = squeak.HasDecryptionKey()
    content_str = squeak.GetDecryptedContentStr() if is_unlocked else None
    squeak_profile = squeak_entry_with_profile.squeak_profile
    is_author_known = squeak_profile is not None
    author_name = squeak_profile.profile_name if squeak_profile else None
    author_address = str(squeak.GetAddress())
    is_reply = squeak.is_reply
    reply_to = squeak.hashReplySqk.hex() if is_reply else None
    return squeak_admin_pb2.SqueakDisplayEntry(
        squeak_hash=get_hash(squeak).hex(),
        is_unlocked=squeak.HasDecryptionKey(),
        content_str=content_str,
        block_height=squeak.nBlockHeight,
        block_hash=squeak.hashBlock.hex(),
        block_time=block_header.nTime,
        is_author_known=is_author_known,
        author_name=author_name,
        author_address=author_address,
        is_reply=is_reply,
        reply_to=reply_to,
    )


def squeak_profile_to_message(squeak_profile):
    if squeak_profile is None:
        return None
    has_private_key = squeak_profile.private_key is not None
    return squeak_admin_pb2.SqueakProfile(
        profile_id=squeak_profile.profile_id,
        profile_name=squeak_profile.profile_name,
        has_private_key=has_private_key,
        address=squeak_profile.address,
        sharing=squeak_profile.sharing,
        following=squeak_profile.following,
    )


def squeak_peer_to_message(squeak_peer):
    if squeak_peer is None:
        return None
    return squeak_admin_pb2.SqueakPeer(
        peer_id=squeak_peer.peer_id,
        peer_name=squeak_peer.peer_name,
        host=squeak_peer.host,
        port=squeak_peer.port,
        uploading=squeak_peer.uploading,
        downloading=squeak_peer.downloading,
    )


def offer_entry_to_message(received_offer_entry: ReceivedOfferWithPeer):
    if received_offer_entry is None:
        return None
    received_offer = received_offer_entry.received_offer
    peer = squeak_peer_to_message(received_offer_entry.peer)
    return squeak_admin_pb2.OfferDisplayEntry(
        offer_id=received_offer.received_offer_id,
        squeak_hash=received_offer.squeak_hash.hex(),
        price_msat=received_offer.price_msat,
        node_pubkey=received_offer.destination,
        node_host=received_offer.node_host,
        node_port=received_offer.node_port,
        peer=peer,
        invoice_timestamp=received_offer.invoice_timestamp,
        invoice_expiry=received_offer.invoice_expiry,
    )


def sent_payment_with_peer_to_message(sent_payment_with_peer):
    if sent_payment_with_peer is None:
        return None
    sent_payment = sent_payment_with_peer.sent_payment
    peer = sent_payment_with_peer.peer
    return squeak_admin_pb2.SentPayment(
        sent_payment_id=sent_payment.sent_payment_id,
        peer_id=sent_payment.peer_id,
        peer_name=peer.peer_name,
        squeak_hash=sent_payment.squeak_hash.hex(),
        payment_hash=sent_payment.payment_hash.hex(),
        price_msat=sent_payment.price_msat,
        node_pubkey=sent_payment.node_pubkey,
        valid=sent_payment.valid,
        time_s=int(sent_payment.created.timestamp()),
    )


def sync_result_to_message(sync_result):
    if sync_result is None:
        return None
    return squeak_admin_pb2.SyncResult(
        completed_peer_ids=sync_result.completed_peer_ids,
        failed_peer_ids=sync_result.failed_peer_ids,
        timeout_peer_ids=sync_result.timeout_peer_ids,
    )


def squeak_entry_to_detail_message(squeak_entry_with_profile: SqueakEntryWithProfile):
    if squeak_entry_with_profile is None:
        return None
    squeak_entry = squeak_entry_with_profile.squeak_entry
    squeak = squeak_entry.squeak
    # block_header = squeak_entry.block_header
    # is_unlocked = squeak.HasDecryptionKey()
    # content_str = squeak.GetDecryptedContentStr() if is_unlocked else None
    # squeak_profile = squeak_entry_with_profile.squeak_profile
    # is_author_known = squeak_profile is not None
    # author_name = squeak_profile.profile_name if squeak_profile else None
    # author_address = str(squeak.GetAddress())
    # is_reply = squeak.is_reply
    # reply_to = get_replyto(squeak) if is_reply else None
    serialized_squeak = squeak.serialize()
    return squeak_admin_pb2.SqueakDetailEntry(
        serialized_squeak_hex=serialized_squeak.hex(),
    )


def sent_offer_to_message(sent_offer):
    if sent_offer is None:
        return None
    return squeak_admin_pb2.SentOffer(
        sent_offer_id=sent_offer.sent_offer_id,
        squeak_hash=sent_offer.squeak_hash.hex(),
        payment_hash=sent_offer.payment_hash.hex(),
        price_msat=sent_offer.price_msat,
    )


def received_payments_to_message(received_payment):
    if received_payment is None:
        return None
    return squeak_admin_pb2.ReceivedPayment(
        received_payment_id=received_payment.received_payment_id,
        squeak_hash=received_payment.squeak_hash.hex(),
        payment_hash=received_payment.payment_hash.hex(),
        price_msat=received_payment.price_msat,
        time_s=int(received_payment.created.timestamp()),
        client_addr=received_payment.client_addr,
    )


def payment_summary_to_message(
        received_payment_summary: ReceivedPaymentSummary,
        sent_payment_summary: SentPaymentSummary,
):
    return squeak_admin_pb2.PaymentSummary(
        num_received_payments=received_payment_summary.num_received_payments,
        num_sent_payments=sent_payment_summary.num_sent_payments,
        amount_earned_msat=received_payment_summary.total_amount_received_msat,
        amount_spent_msat=sent_payment_summary.total_amount_sent_msat,
    )
