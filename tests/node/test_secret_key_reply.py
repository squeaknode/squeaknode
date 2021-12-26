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
from squeak.messages import msg_secretkey
from squeak.net import COffer

from squeaknode.node.secret_key_reply import FreeSecretKeyReply
from squeaknode.node.secret_key_reply import OfferReply


@pytest.fixture()
def free_secret_key_reply(squeak_hash, secret_key):
    yield FreeSecretKeyReply(
        squeak_hash=squeak_hash,
        secret_key=secret_key,
    )


@pytest.fixture()
def offer_reply(squeak_hash, offer):
    yield OfferReply(
        squeak_hash=squeak_hash,
        offer=offer,
    )


def test_free_secret_key_reply_msg(squeak_hash, secret_key, free_secret_key_reply):
    reply_msg = free_secret_key_reply.get_msg()

    assert reply_msg == msg_secretkey(
        hashSqk=squeak_hash,
        secretKey=secret_key,
    )


def test_offer_reply_msg(squeak_hash, offer, offer_reply):
    reply_msg = offer_reply.get_msg()

    assert reply_msg == msg_secretkey(
        hashSqk=squeak_hash,
        offer=COffer(
            nonce=offer.nonce,
            strPaymentInfo=offer.payment_request.encode(
                'utf-8'),
            host=offer.host.encode('utf-8'),
            port=offer.port,
        )
    )
