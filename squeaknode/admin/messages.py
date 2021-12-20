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

from squeak.core.signing import SqueakPublicKey

from proto import squeak_admin_pb2
from squeaknode.admin.profile_image_util import bytes_to_base64_string
from squeaknode.admin.profile_image_util import load_default_profile_image
from squeaknode.core.connected_peer import ConnectedPeer
from squeaknode.core.download_result import DownloadResult
from squeaknode.core.peer_address import Network
from squeaknode.core.peer_address import PeerAddress
from squeaknode.core.received_offer import ReceivedOffer
from squeaknode.core.received_payment import ReceivedPayment
from squeaknode.core.received_payment_summary import ReceivedPaymentSummary
from squeaknode.core.sent_offer import SentOffer
from squeaknode.core.sent_payment import SentPayment
from squeaknode.core.sent_payment_summary import SentPaymentSummary
from squeaknode.core.squeak_entry import SqueakEntry
from squeaknode.core.squeak_peer import SqueakPeer
from squeaknode.core.squeak_profile import SqueakProfile
from squeaknode.core.twitter_account_entry import TwitterAccountEntry

logger = logging.getLogger(__name__)


DEFAULT_PROFILE_IMAGE = load_default_profile_image()


def squeak_entry_to_message(squeak_entry: SqueakEntry) -> squeak_admin_pb2.SqueakDisplayEntry:
    squeak_profile = squeak_entry.squeak_profile
    secret_key = squeak_entry.secret_key.hex() if squeak_entry.secret_key else None
    is_reply = bool(squeak_entry.reply_to)
    reply_to = squeak_entry.reply_to.hex() if squeak_entry.reply_to else None
    is_author_known = False
    profile_msg = None
    if squeak_profile is not None:
        is_author_known = True
        profile_msg = squeak_profile_to_message(squeak_profile)
    return squeak_admin_pb2.SqueakDisplayEntry(
        squeak_hash=squeak_entry.squeak_hash.hex(),
        serialized_squeak_hex=squeak_entry.serialized_squeak.hex(),
        is_unlocked=squeak_entry.is_unlocked,
        secret_key_hex=secret_key,  # type: ignore
        content_str=squeak_entry.content,  # type: ignore
        block_height=squeak_entry.block_height,
        block_hash=squeak_entry.block_hash.hex(),
        block_time=squeak_entry.block_time,
        squeak_time=squeak_entry.squeak_time,
        is_reply=is_reply,
        reply_to=reply_to,  # type: ignore
        author_pubkey=squeak_entry.public_key.to_bytes().hex(),
        is_author_known=is_author_known,
        author=profile_msg,
        liked_time_ms=squeak_entry.liked_time_ms,  # type: ignore
    )


def squeak_profile_to_message(squeak_profile: SqueakProfile) -> squeak_admin_pb2.SqueakProfile:
    profile_id = squeak_profile.profile_id or 0
    has_private_key = squeak_profile.private_key is not None
    profile_image = squeak_profile.profile_image or DEFAULT_PROFILE_IMAGE
    has_custom_profile_image = squeak_profile.profile_image is not None
    image_base64_str = bytes_to_base64_string(profile_image)
    return squeak_admin_pb2.SqueakProfile(
        profile_id=profile_id,
        profile_name=squeak_profile.profile_name,
        has_private_key=has_private_key,
        pubkey=squeak_profile.public_key.to_bytes().hex(),
        following=squeak_profile.following,
        profile_image=image_base64_str,
        has_custom_profile_image=has_custom_profile_image,
    )


def squeak_peer_to_message(squeak_peer: SqueakPeer) -> squeak_admin_pb2.SqueakPeer:
    peer_id = squeak_peer.peer_id or 0
    return squeak_admin_pb2.SqueakPeer(
        peer_id=peer_id,
        peer_name=squeak_peer.peer_name,
        peer_address=peer_address_to_message(squeak_peer.address),
        autoconnect=squeak_peer.autoconnect,
        share_for_free=squeak_peer.share_for_free,
    )


def received_offer_to_message(received_offer: ReceivedOffer) -> squeak_admin_pb2.OfferDisplayEntry:
    received_offer_id = received_offer.received_offer_id or 0
    return squeak_admin_pb2.OfferDisplayEntry(
        offer_id=received_offer_id,
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
    sent_payment_id = sent_payment.sent_payment_id or 0
    created_time_ms = sent_payment.created_time_ms or 0
    return squeak_admin_pb2.SentPayment(
        sent_payment_id=sent_payment_id,
        squeak_hash=sent_payment.squeak_hash.hex(),
        payment_hash=sent_payment.payment_hash.hex(),
        price_msat=sent_payment.price_msat,
        node_pubkey=sent_payment.node_pubkey,
        valid=sent_payment.valid,
        time_ms=created_time_ms,
        peer_address=peer_address_to_message(sent_payment.peer_address)
    )


def sent_offer_to_message(sent_offer: SentOffer) -> squeak_admin_pb2.SentOffer:
    sent_offer_id = sent_offer.sent_offer_id or 0
    return squeak_admin_pb2.SentOffer(
        sent_offer_id=sent_offer_id,
        squeak_hash=sent_offer.squeak_hash.hex(),
        payment_hash=sent_offer.payment_hash.hex(),
        price_msat=sent_offer.price_msat,
    )


def received_payment_to_message(received_payment: ReceivedPayment) -> squeak_admin_pb2.ReceivedPayment:
    received_payment_id = received_payment.received_payment_id or 0
    created_time_ms = received_payment.created_time_ms or 0
    return squeak_admin_pb2.ReceivedPayment(
        received_payment_id=received_payment_id,
        squeak_hash=received_payment.squeak_hash.hex(),
        payment_hash=received_payment.payment_hash.hex(),
        price_msat=received_payment.price_msat,
        time_ms=created_time_ms,
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


def connected_peer_to_message(connected_peer: ConnectedPeer) -> squeak_admin_pb2.ConnectedPeer:
    peer = connected_peer.peer
    saved_peer = connected_peer.saved_peer
    is_peer_saved = saved_peer is not None
    saved_peer_msg = None
    if saved_peer is not None:
        saved_peer_msg = squeak_peer_to_message(saved_peer)
    return squeak_admin_pb2.ConnectedPeer(
        peer_address=peer_address_to_message(peer.remote_address),
        connect_time_s=peer.connect_time,
        last_message_received_time_s=peer.last_msg_revc_time,
        number_messages_received=peer.num_msgs_received,
        number_bytes_received=peer.num_bytes_received,
        number_messages_sent=peer.num_msgs_sent,
        number_bytes_sent=peer.num_bytes_sent,
        is_peer_saved=is_peer_saved,
        saved_peer=saved_peer_msg,
    )


def peer_address_to_message(peer_address: PeerAddress) -> squeak_admin_pb2.PeerAddress:
    return squeak_admin_pb2.PeerAddress(
        network=peer_address.network.name,
        host=peer_address.host,
        port=peer_address.port,
    )


def message_to_peer_address(msg: squeak_admin_pb2.PeerAddress) -> PeerAddress:
    return PeerAddress(
        network=Network[msg.network],
        host=msg.host,
        port=msg.port,
    )


def message_to_squeak_entry(msg: squeak_admin_pb2.SqueakDisplayEntry) -> SqueakEntry:
    like_time_ms = msg.liked_time_ms if msg.liked_time_ms > 0 else None
    reply_to_hash = bytes.fromhex(msg.reply_to) if msg.reply_to else None
    content_str = msg.content_str if len(msg.content_str) > 0 else None
    secret_key = bytes.fromhex(
        msg.secret_key_hex) if msg.secret_key_hex else None
    return SqueakEntry(
        squeak_hash=bytes.fromhex(msg.squeak_hash),
        serialized_squeak=bytes.fromhex(msg.serialized_squeak_hex),
        public_key=SqueakPublicKey.from_bytes(
            bytes.fromhex(msg.author_pubkey),
        ),
        block_height=msg.block_height,
        block_hash=bytes.fromhex(msg.block_hash),
        block_time=msg.block_time,
        squeak_time=msg.squeak_time,
        reply_to=reply_to_hash,
        is_unlocked=msg.is_unlocked,
        secret_key=secret_key,
        squeak_profile=None,  # TODO: message to squeak profile
        liked_time_ms=like_time_ms,
        content=content_str,
    )


def message_to_sent_payment(msg: squeak_admin_pb2.SentPayment) -> SentPayment:
    sent_payment_id = msg.sent_payment_id if msg.sent_payment_id > 0 else None
    created_time_ms = msg.time_ms if msg.time_ms > 0 else None
    return SentPayment(
        sent_payment_id=sent_payment_id,
        created_time_ms=created_time_ms,
        peer_address=message_to_peer_address(msg.peer_address),
        squeak_hash=bytes.fromhex(msg.squeak_hash),
        payment_hash=bytes.fromhex(msg.payment_hash),
        secret_key=b'',  # TODO: why does this field exist?
        price_msat=msg.price_msat,
        node_pubkey=msg.node_pubkey,
        valid=msg.valid,
    )


def message_to_received_payment(msg: squeak_admin_pb2.ReceivedPayment) -> ReceivedPayment:
    received_payment_id = msg.received_payment_id if msg.received_payment_id > 0 else None
    created_time_ms = msg.time_ms if msg.time_ms > 0 else None
    return ReceivedPayment(
        received_payment_id=received_payment_id,
        created_time_ms=created_time_ms,
        squeak_hash=bytes.fromhex(msg.squeak_hash),
        payment_hash=bytes.fromhex(msg.payment_hash),
        price_msat=msg.price_msat,
        settle_index=0,  # TODO: This is not correct, fix later.
        peer_address=message_to_peer_address(msg.peer_address),
    )


def download_result_to_message(download_result: DownloadResult) -> squeak_admin_pb2.DownloadResult:
    return squeak_admin_pb2.DownloadResult(
        number_downloaded=download_result.number_downloaded,
        number_requested=download_result.number_requested,
        number_peers=download_result.number_peers,
        elapsed_time_ms=download_result.elapsed_time_ms,
    )


def twitter_account_to_message(twitter_account_entry: TwitterAccountEntry) -> squeak_admin_pb2.TwitterAccount:
    twitter_account_id = twitter_account_entry.twitter_account_id or 0
    squeak_profile = twitter_account_entry.profile
    profile_msg = None
    if squeak_profile is not None:
        profile_msg = squeak_profile_to_message(squeak_profile)
    return squeak_admin_pb2.TwitterAccount(
        twitter_account_id=twitter_account_id,
        handle=twitter_account_entry.handle,
        profile_id=twitter_account_entry.profile_id,
        profile=profile_msg,
    )


def optional_squeak_profile_to_message(squeak_profile: Optional[SqueakProfile]) -> Optional[squeak_admin_pb2.SqueakProfile]:
    if squeak_profile is None:
        return None
    return squeak_profile_to_message(squeak_profile)


def optional_squeak_hash_to_hex(squeak_hash: Optional[bytes]) -> Optional[str]:
    if squeak_hash is None:
        return None
    return squeak_hash.hex()


def optional_squeak_entry_to_message(squeak_entry: Optional[SqueakEntry]) -> Optional[squeak_admin_pb2.SqueakDisplayEntry]:
    if squeak_entry is None:
        return None
    return squeak_entry_to_message(squeak_entry)


def optional_squeak_peer_to_message(squeak_peer: Optional[SqueakPeer]) -> Optional[squeak_admin_pb2.SqueakPeer]:
    if squeak_peer is None:
        return None
    return squeak_peer_to_message(squeak_peer)


def optional_received_offer_to_message(received_offer: Optional[ReceivedOffer]) -> Optional[squeak_admin_pb2.OfferDisplayEntry]:
    if received_offer is None:
        return None
    return received_offer_to_message(received_offer)


def optional_sent_payment_to_message(sent_payment: Optional[SentPayment]) -> Optional[squeak_admin_pb2.SentPayment]:
    if sent_payment is None:
        return None
    return sent_payment_to_message(sent_payment)


def optional_connected_peer_to_message(connected_peer: Optional[ConnectedPeer]) -> Optional[squeak_admin_pb2.ConnectedPeer]:
    if connected_peer is None:
        return None
    return connected_peer_to_message(connected_peer)
