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
import hashlib
import os
import uuid

from bitcoin.core import CBlockHeader
from squeak.core.signing import CSigningKey
from squeak.core.signing import CSqueakAddress

from squeaknode.core.profiles import create_contact_profile
from squeaknode.core.profiles import create_signing_profile
from squeaknode.core.squeaks import HASH_LENGTH
from squeaknode.core.squeaks import make_squeak_with_block


def gen_signing_key():
    return CSigningKey.generate()


def gen_random_hash():
    return os.urandom(HASH_LENGTH)


def sha256(data):
    return hashlib.sha256(data).digest()


def address_from_signing_key(signing_key):
    verifying_key = signing_key.get_verifying_key()
    return CSqueakAddress.from_verifying_key(verifying_key)


def gen_address():
    signing_key = gen_signing_key()
    return address_from_signing_key(signing_key)


def gen_squeak_addresses(n):
    return [gen_address() for i in range(n)]


def gen_squeak(signing_key, block_height, replyto_hash=None):
    random_content = "random_content_{}".format(uuid.uuid1())
    random_hash = gen_random_hash()
    squeak, secret_key = make_squeak_with_block(
        signing_key,
        random_content,
        block_height,
        random_hash,
        replyto_hash=replyto_hash,
    )
    return squeak


def gen_block_header(block_height):
    return CBlockHeader(
        nTime=block_height * 10,  # So that block times are increasing.
    )


def gen_squeak_with_block_header(signing_key, block_height, replyto_hash=None):
    """ Return a tuple with a CSqueak and a CBlockHeader.
    """
    squeak = gen_squeak(
        signing_key=signing_key,
        block_height=block_height,
        replyto_hash=replyto_hash,
    )
    block_info = gen_block_header(
        block_height=block_height,
    )
    return squeak, block_info


def gen_signing_profile(profile_name, signing_key):
    return create_signing_profile(
        profile_name,
        signing_key,
    )


def gen_contact_profile(profile_name, address):
    return create_contact_profile(
        profile_name,
        address,
    )
