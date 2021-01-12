import os

from bitcoin.base58 import Base58ChecksumError
from bitcoin.wallet import CBitcoinAddressError
from squeak.core.elliptic import generate_random_scalar
from squeak.core.elliptic import scalar_difference
from squeak.core.elliptic import scalar_from_bytes
from squeak.core.elliptic import scalar_sum
from squeak.core.elliptic import scalar_to_bytes
from squeak.core.signing import CSqueakAddress

DATA_KEY_LENGTH = 32


def get_hash(squeak):
    # hash_bytes = squeak.GetHash()[::-1]
    # return hash_bytes.hex()
    return squeak.GetHash()[::-1]


def get_replyto(squeak):
    return squeak.hashReplySqk.hex()


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
