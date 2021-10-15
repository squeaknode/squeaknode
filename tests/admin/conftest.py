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
import pytest

from proto import squeak_admin_pb2
from squeaknode.admin.messages import DEFAULT_PROFILE_IMAGE
from squeaknode.admin.profile_image_util import bytes_to_base64_string


@pytest.fixture
def peer_address_message():
    yield squeak_admin_pb2.PeerAddress(
        network="IPV4",
        host="fake_host",
        port=8765,
    )


@pytest.fixture
def default_profile_image():
    yield DEFAULT_PROFILE_IMAGE


@pytest.fixture
def signing_profile_msg(
        address_str,
        default_profile_image,
):
    img_base64_str = bytes_to_base64_string(default_profile_image)
    yield squeak_admin_pb2.SqueakProfile(
        profile_id=None,
        profile_name="fake_signing_profile_name",
        has_private_key=True,
        address=address_str,
        following=True,
        use_custom_price=False,
        custom_price_msat=0,
        profile_image=img_base64_str,
        has_custom_profile_image=False,
    )


@pytest.fixture
def squeak_entry_msg_locked(
        squeak,
        squeak_hash,
        address_str,
        block_count,
        block_hash,
        block_time,
        squeak_time,
        squeak_reply_to_hash,
        signing_profile_msg,
):
    yield squeak_admin_pb2.SqueakDisplayEntry(
        squeak_hash=squeak_hash.hex(),
        is_unlocked=False,
        content_str=None,  # type: ignore
        block_height=block_count,
        block_hash=block_hash.hex(),
        block_time=block_time,
        squeak_time=squeak_time,
        is_reply=False,
        reply_to=squeak_reply_to_hash,  # type: ignore
        author_address=address_str,
        is_author_known=True,
        author=signing_profile_msg,
        liked_time_ms=None,  # type: ignore
    )


@pytest.fixture
def peer_msg(
        peer_name,
        peer_address_message,
):
    yield squeak_admin_pb2.SqueakPeer(
        peer_id=None,
        peer_name=peer_name,
        peer_address=peer_address_message,
        autoconnect=False,
    )


@pytest.fixture
def received_offer_msg(
        squeak_hash,
        price_msat,
        creation_date,
        expiry,
        payment_request,
        seller_pubkey,
        lightning_address,
        peer_address_message,
):
    return squeak_admin_pb2.OfferDisplayEntry(
        offer_id=None,
        squeak_hash=squeak_hash.hex(),
        price_msat=price_msat,
        node_pubkey=seller_pubkey,
        node_host=lightning_address.host,
        node_port=lightning_address.port,
        invoice_timestamp=creation_date,
        invoice_expiry=expiry,
        peer_address=peer_address_message,
    )
