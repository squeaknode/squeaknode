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
import os
import random
from typing import Iterable

from bitcoin.base58 import Base58ChecksumError
from bitcoin.wallet import CBitcoinAddressError
from squeak.core import CSqueak
from squeak.core.elliptic import generate_random_scalar
from squeak.core.elliptic import scalar_difference
from squeak.core.elliptic import scalar_from_bytes
from squeak.core.elliptic import scalar_sum
from squeak.core.elliptic import scalar_to_bytes
from squeak.core.signing import CSqueakAddress
from squeak.net import CInterested


DATA_KEY_LENGTH = 32
VERSION_NONCE_LENGTH = 8

HASH_LENGTH = 32
EMPTY_HASH = b'\x00' * HASH_LENGTH


def get_hash(squeak):
    return squeak.GetHash()[::-1]


def generate_version_nonce() -> int:
    return random.SystemRandom().getrandbits(64)


def generate_ping_nonce() -> int:
    return random.SystemRandom().getrandbits(64)


def generate_offer_nonce():
    return os.urandom(DATA_KEY_LENGTH)


def generate_offer_preimage():
    return os.urandom(DATA_KEY_LENGTH)


def generate_tweak():
    tweak = generate_random_scalar()
    return scalar_to_bytes(tweak)


def bxor(b1, b2):  # use xor for bytes
    result = bytearray()
    for b1, b2 in zip(b1, b2):
        result.append(b1 ^ b2)
    return bytes(result)


def add_tweak(n, tweak):
    n_int = scalar_from_bytes(n)
    tweak_int = scalar_from_bytes(tweak)
    sum_int = scalar_sum(n_int, tweak_int)
    return scalar_to_bytes(sum_int)


def subtract_tweak(n, tweak):
    n_int = scalar_from_bytes(n)
    tweak_int = scalar_from_bytes(tweak)
    sum_int = scalar_difference(n_int, tweak_int)
    return scalar_to_bytes(sum_int)


def is_address_valid(address: str) -> bool:
    if not address:
        return False
    try:
        CSqueakAddress(address)
    except (Base58ChecksumError, CBitcoinAddressError):
        return False
    return True


def squeak_matches_interest(squeak: CSqueak, interest: CInterested) -> bool:
    if len(interest.addresses) > 0 \
       and squeak.GetAddress() not in interest.addresses:
        return False
    if interest.nMinBlockHeight != -1 \
       and squeak.nBlockHeight < interest.nMinBlockHeight:
        return False
    if interest.nMaxBlockHeight != -1 \
       and squeak.nBlockHeight > interest.nMaxBlockHeight:
        return False
    if interest.hashReplySqk != EMPTY_HASH \
       and squeak.hashReplySqk != interest.hashReplySqk:
        return False
    return True


def get_differential_squeaks(
        interest: CInterested,
        old_interest: CInterested,
) -> Iterable[CInterested]:
    # Get new squeaks below the current min_block
    if interest.nMinBlockHeight < old_interest.nMinBlockHeight:
        yield CInterested(
            addresses=old_interest.addresses,
            nMinBlockHeight=interest.nMinBlockHeight,
            nMaxBlockHeight=old_interest.nMinBlockHeight - 1,
        )
    # Get new squeaks above the current max_block
    if (interest.nMaxBlockHeight == -1 and old_interest.nMaxBlockHeight != -1) or \
       interest.nMaxBlockHeight > old_interest.nMaxBlockHeight:
        yield CInterested(
            addresses=old_interest.addresses,
            nMinBlockHeight=old_interest.nMaxBlockHeight + 1,
            nMaxBlockHeight=interest.nMaxBlockHeight,
        )
    # Get new squeaks for new addresses
    follow_addresses = set(interest.addresses)
    old_follow_addresses = set(old_interest.addresses)
    new_addresses = tuple(follow_addresses - old_follow_addresses)
    if len(new_addresses) > 0:
        yield CInterested(
            addresses=new_addresses,
            nMinBlockHeight=interest.nMinBlockHeight,
            nMaxBlockHeight=interest.nMaxBlockHeight,
        )
