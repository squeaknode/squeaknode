import time

import pytest
from bitcoin.core import lx
from squeak.core import HASH_LENGTH
from squeak.core import MakeSqueakFromStr
from squeak.core.signing import CSigningKey

from squeaknode.server.squeak_validator import SqueakValidator

# # read in SQL for populating test data
# with open(os.path.join(os.path.dirname(__file__), "data.sql"), "rb") as f:
#     _data_sql = f.read().decode("utf8")


def make_squeak(
    signing_key: CSigningKey, content: str, reply_to: bytes = b"\x00" * HASH_LENGTH
):
    block_height = 0
    block_hash = lx(
        "4a5e1e4baab89f3a32518a88c31bc87f618f76673e2cc77ab2127b7afdeda33b")
    timestamp = int(time.time())
    return MakeSqueakFromStr(
        signing_key,
        content,
        block_height,
        block_hash,
        timestamp,
    )


@pytest.fixture
def signing_key():
    return CSigningKey.generate()


@pytest.fixture
def validator():
    return SqueakValidator()


@pytest.fixture
def example_squeak(signing_key):
    return make_squeak(
        signing_key,
        "hello!",
    )


@pytest.fixture
def bad_squeak(signing_key):
    squeak = make_squeak(
        signing_key,
        "hello!",
    )
    squeak.ClearDecryptionKey()
    return squeak
