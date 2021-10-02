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

from bitcoin.base58 import Base58ChecksumError
from bitcoin.wallet import CBitcoinAddressError
from squeak.core.elliptic import generate_random_scalar
from squeak.core.elliptic import scalar_difference
from squeak.core.elliptic import scalar_from_bytes
from squeak.core.elliptic import scalar_sum
from squeak.core.elliptic import scalar_to_bytes
from squeak.core.signing import CSqueakAddress


DATA_KEY_LENGTH = 32
VERSION_NONCE_LENGTH = 8

HASH_LENGTH = 32
EMPTY_HASH = b'\x00' * HASH_LENGTH


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
