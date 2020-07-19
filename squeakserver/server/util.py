import os

DATA_KEY_LENGTH = 32


def get_hash(squeak):
    return squeak.GetHash()[::-1]


def generate_offer_nonce():
    return os.urandom(DATA_KEY_LENGTH)


def generate_offer_preimage():
    return os.urandom(DATA_KEY_LENGTH)


def bxor(b1, b2):  # use xor for bytes
    result = bytearray()
    for b1, b2 in zip(b1, b2):
        result.append(b1 ^ b2)
    return bytes(result)
