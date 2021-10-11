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
from squeaknode.core.peer_address import Network
from squeaknode.core.peer_address import PeerAddress
from squeaknode.core.squeak_core import SqueakCore
from squeaknode.core.squeaks import get_hash
from squeaknode.lightning.invoice import Invoice
from squeaknode.lightning.lightning_client import LightningClient
from tests.utils import gen_random_hash


@pytest.fixture
def lightning_host_port():
    return LightningAddressHostPort(host="my_lightning_host", port=8765)


@pytest.fixture
def price_msat():
    return 777


@pytest.fixture
def preimage():
    yield gen_random_hash()


@pytest.fixture
def payment_hash(preimage):
    # TODO: This should be the hash of the preimage
    yield gen_random_hash()


@pytest.fixture
def payment_request():
    yield "fake_payment_request"


@pytest.fixture
def creation_date():
    yield 777777


@pytest.fixture
def expiry():
    yield 5555


@pytest.fixture
def invoice(payment_hash, payment_request, price_msat, creation_date, expiry):
    yield Invoice(
        r_hash=payment_hash,
        payment_request=payment_request,
        value_msat=price_msat,
        settled=False,
        settle_index=0,
        creation_date=creation_date,
        expiry=expiry,
    )


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

    def __init__(self, invoice):
        self.invoice = invoice

    def get_info(self):
        pass

    def create_invoice(self, preimage: bytes, amount_msat: int):
        return self.invoice

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
def lightning_client(invoice):
    return MockLightningClient(invoice)


@pytest.fixture
def squeak_core(bitcoin_client, lightning_client):
    yield SqueakCore(bitcoin_client, lightning_client)


@pytest.fixture
def squeak_and_decryption_key(squeak_core, signing_profile, squeak_content):
    yield squeak_core.make_squeak(
        signing_profile,
        squeak_content,
    )


@pytest.fixture
def squeak(squeak_and_decryption_key):
    squeak, _ = squeak_and_decryption_key
    yield squeak


@pytest.fixture
def decryption_key(squeak_and_decryption_key):
    _, decryption_key = squeak_and_decryption_key
    yield decryption_key


@pytest.fixture
def peer_address():
    yield PeerAddress(
        network=Network.IPV4,
        host="fake_host",
        port=8765,
    )


def test_get_block_header(
        squeak_core,
        squeak,
        genesis_block_info,
):
    block_header = squeak_core.get_block_header(squeak)

    assert block_header == genesis_block_info.block_header


def test_get_decrypted_content(squeak_core, squeak, decryption_key, squeak_content):
    decrypted_content = squeak_core.get_decrypted_content(
        squeak,
        decryption_key,
    )

    assert decrypted_content == squeak_content


def test_get_best_block_height(squeak_core, genesis_block_info):
    best_block_height = squeak_core.get_best_block_height()

    assert best_block_height == genesis_block_info.block_height


def test_create_offer(squeak_core, squeak, decryption_key, peer_address, price_msat, invoice):
    created_sent_offer = squeak_core.create_offer(
        squeak,
        decryption_key,
        peer_address,
        price_msat,
    )

    assert created_sent_offer.squeak_hash == get_hash(squeak)
    assert created_sent_offer.payment_hash == invoice.r_hash
    # assert created_sent_offer.secret_key == decryption_key
    assert created_sent_offer.price_msat == price_msat
    assert created_sent_offer.payment_request == invoice.payment_request
    assert created_sent_offer.invoice_time == invoice.creation_date
    assert created_sent_offer.invoice_expiry == invoice.expiry
    assert created_sent_offer.peer_address == peer_address
