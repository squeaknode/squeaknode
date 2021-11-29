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
from squeak.messages import msg_offer
from squeak.messages import msg_secretkey
from squeak.messages import MsgSerializable

from squeaknode.core.offer import Offer


class SecretKeyReply:

    def get_msg(self) -> MsgSerializable:
        """Return the message to reply to the other peer.
        """


class FreeSecretKeyReply(SecretKeyReply):

    def __init__(self, squeak_hash: bytes, secret_key: bytes):
        self.squeak_hash = squeak_hash
        self.secret_key = secret_key

    def get_msg(self) -> MsgSerializable:
        return msg_secretkey(
            hashSqk=self.squeak_hash,
            secretKey=self.secret_key,
        )


class OfferReply(SecretKeyReply):

    def __init__(self, squeak_hash: bytes, offer: Offer):
        self.squeak_hash = squeak_hash
        self.offer = offer

    def get_msg(self) -> MsgSerializable:
        return msg_offer(
            hashSqk=self.squeak_hash,
            nonce=self.offer.nonce,
            strPaymentInfo=self.offer.payment_request.encode(
                'utf-8'),
            host=self.offer.host.encode('utf-8'),
            port=self.offer.port,
        )
