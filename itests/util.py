import time

from bitcoin.core import lx
from squeak.core import HASH_LENGTH, MakeSqueakFromStr
from squeak.core.signing import CSigningKey


def generate_signing_key():
    return CSigningKey.generate()


def make_squeak(
    signing_key: CSigningKey, content: str, reply_to: bytes = b"\x00" * HASH_LENGTH
):
    block_height = 0
    block_hash = lx("4a5e1e4baab89f3a32518a88c31bc87f618f76673e2cc77ab2127b7afdeda33b")
    timestamp = int(time.time())
    return MakeSqueakFromStr(
        signing_key,
        content,
        block_height,
        block_hash,
        timestamp,
    )
