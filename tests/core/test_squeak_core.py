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
import pytest

from squeaknode.bitcoin.bitcoin_client import BitcoinClient
from squeaknode.bitcoin.block_info import BlockInfo
from squeaknode.core.lightning_address import LightningAddressHostPort
from squeaknode.core.squeak_core import SqueakCore
from squeaknode.lightning.lightning_client import LightningClient


@pytest.fixture
def lightning_host_port():
    return LightningAddressHostPort(host="my_lightning_host", port=8765)


@pytest.fixture
def price_msat():
    return 777


class MockBitcoinClient(BitcoinClient):

    def __init__(self, best_block_info):
        self.best_block_info = best_block_info

    def get_best_block_info(self) -> BlockInfo:
        return self.best_block_info

    def get_block_info_by_height(self, block_height: int) -> BlockInfo:
        if block_height == 0:
            return self.best_block_info
        else:
            raise Exception("Invalid block height")

    def get_block_hash(self, block_height: int) -> bytes:
        if block_height == 0:
            return self.best_block_info.block_hash
        else:
            raise Exception("Invalid block height")

    def get_block_header(self, block_hash: bytes, verbose: bool) -> bytes:
        if block_hash == self.best_block_info.block_hash:
            return self.best_block_info.block_header
        else:
            raise Exception("Invalid block hash")


class MockLightningClient(LightningClient):

    def get_info(self):
        pass

    def create_invoice(self, preimage: bytes, amount_msat: int):
        pass

    def decode_pay_req(self, payment_request: str):
        pass

    def pay_invoice(self, payment_request: str):
        pass

    def subscribe_invoices(self, settle_index: int):
        pass


@pytest.fixture
def bitcoin_client(genesis_block_info):
    return MockBitcoinClient(genesis_block_info)


@pytest.fixture
def lightning_client():
    return MockLightningClient()


@pytest.fixture
def squeak_core(bitcoin_client, lightning_client):
    yield SqueakCore(bitcoin_client, lightning_client)


def test_make_squeak(
        squeak_core,
        signing_profile,
        squeak_content,
):
    squeak, decryption_key = squeak_core.make_squeak(
        signing_profile,
        squeak_content,
    )

    assert squeak.GetDecryptedContentStr(decryption_key) == squeak_content


# def test_get_block_header(
#         squeak_core,
#         signing_profile,
#         squeak_content,
# ):
#     squeak_core = SqueakCore(bitcoin_client, lightning_client)
#     squeak, decryption_key = squeak_core.make_squeak(
#         signing_profile,
#         content_str,
#     )

#     assert squeak.GetDecryptedContentStr(decryption_key) == content_str
#     assert not squeak.is_reply
