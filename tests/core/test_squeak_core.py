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
import mock
import pytest
from bitcoin.core import CoreMainParams
from squeak.core.signing import CSigningKey
from squeak.core.signing import CSqueakAddress

from squeaknode.bitcoin.bitcoin_client import BitcoinClient
from squeaknode.bitcoin.block_info import BlockInfo
from squeaknode.core.lightning_address import LightningAddressHostPort
from squeaknode.core.squeak_core import SqueakCore
from squeaknode.core.squeak_profile import SqueakProfile


@pytest.fixture
def lightning_client():
    return mock.Mock()


@pytest.fixture
def lightning_host_port():
    return LightningAddressHostPort(host="my_lightning_host", port=8765)


@pytest.fixture
def price_msat():
    return 777


class MockBitcoinClient(BitcoinClient):
    genesis_block_info = BlockInfo(
        block_height=0,
        block_hash=CoreMainParams.GENESIS_BLOCK.GetHash(),
        block_header=CoreMainParams.GENESIS_BLOCK.get_header().serialize(),
    )

    def get_best_block_info(self) -> BlockInfo:
        return self.genesis_block_info

    def get_block_info_by_height(self, block_height: int) -> BlockInfo:
        if block_height == 0:
            return self.genesis_block_info
        else:
            raise Exception("Invalid block height")

    def get_block_hash(self, block_height: int) -> bytes:
        if block_height == 0:
            return self.genesis_block_info.block_hash
        else:
            raise Exception("Invalid block height")

    def get_block_header(self, block_hash: bytes, verbose: bool) -> bytes:
        if block_hash == self.genesis_block_info.block_hash:
            return self.genesis_block_info.block_header
        else:
            raise Exception("Invalid block hash")


@pytest.fixture
def signing_profile():
    profile_name = "fake_name"
    signing_key = CSigningKey.generate()
    verifying_key = signing_key.get_verifying_key()
    address = CSqueakAddress.from_verifying_key(verifying_key)
    signing_key_str = str(signing_key)
    signing_key_bytes = signing_key_str.encode()
    return SqueakProfile(
        profile_id=None,
        profile_name=profile_name,
        private_key=signing_key_bytes,
        address=str(address),
        following=False,
        use_custom_price=False,
        custom_price_msat=0,
        profile_image=None,
    )


@pytest.fixture
def bitcoin_client():
    return MockBitcoinClient()


def test_make_squeak(bitcoin_client, lightning_client, signing_profile):
    squeak_core = SqueakCore(bitcoin_client, lightning_client)
    squeak, decryption_key = squeak_core.make_squeak(signing_profile, "hello")

    assert squeak.GetDecryptedContentStr(decryption_key) == "hello"


# def test_pay_offer(bitcoin_client, lightning_client, signing_profile):
#     squeak_core = SqueakCore(bitcoin_client, lightning_client)
#     squeak_entry = squeak_core.make_squeak(signing_profile, "hello")

#     assert squeak_entry.squeak.GetDecryptedContentStr() == "hello"

#     validated_squeak_entry = squeak_core.validate_squeak(squeak_entry.squeak)

#     assert validated_squeak_entry == squeak_entry
