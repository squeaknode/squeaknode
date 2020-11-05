import os

DATA_KEY_LENGTH = 32


def get_hash(squeak):
    hash_bytes = squeak.GetHash()[::-1]
    return hash_bytes.hex()


def get_replyto(squeak):
    return squeak.hashReplySqk.hex()


def generate_offer_nonce():
    return os.urandom(DATA_KEY_LENGTH)


def generate_offer_preimage():
    return os.urandom(DATA_KEY_LENGTH)


def bxor(b1, b2):  # use xor for bytes
    result = bytearray()
    for b1, b2 in zip(b1, b2):
        result.append(b1 ^ b2)
    return bytes(result)
