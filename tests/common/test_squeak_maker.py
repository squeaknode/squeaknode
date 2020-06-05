import os

import pytest
from squeak.core import CheckSqueak
from squeak.core import HASH_LENGTH
from squeak.core.signing import CSigningKey

from squeakserver.common.blockchain_client import BlockchainClient
from squeakserver.common.squeak_maker import SqueakMaker


@pytest.fixture
def signing_key():
    return CSigningKey.generate()


@pytest.fixture
def verifying_key(signing_key):
    return signing_key.get_verifying_key()


@pytest.fixture
def block_height():
    return 56789


@pytest.fixture
def block_hash():
    return os.urandom(HASH_LENGTH)


@pytest.fixture
def blockchain_client(block_height, block_hash):
    return MockBlockchainClient(block_height, block_hash)


class TestSqueakMaker(object):
    def test_make_squeak(self, signing_key, verifying_key, blockchain_client):
        maker = SqueakMaker(signing_key, blockchain_client)
        content = 'Hello world!'
        squeak = maker.make_squeak(content)

        CheckSqueak(squeak)

        assert squeak.nBlockHeight == blockchain_client.get_block_count()
        assert squeak.hashBlock == blockchain_client.get_block_hash(squeak.nBlockHeight)

        decrypted_content = squeak.GetDecryptedContentStr()

        assert decrypted_content == content


class MockBlockchainClient(BlockchainClient):

    def __init__(self, block_height, block_hash):
        self.block_height = block_height
        self.block_hash = block_hash

    def get_block_count(self) -> int:
        return self.block_height

    def get_block_hash(self, block_height: int) -> bytes:
        return self.block_hash
