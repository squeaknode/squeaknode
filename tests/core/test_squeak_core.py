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
from squeaknode.core.secret_keys import add_tweak
from squeaknode.core.secret_keys import generate_tweak
from squeaknode.core.squeak_core import SqueakCore
from squeaknode.core.squeaks import get_hash
from squeaknode.lightning.info import Info
from squeaknode.lightning.invoice import Invoice
from squeaknode.lightning.lightning_client import LightningClient
from squeaknode.lightning.pay_req import PayReq
from squeaknode.lightning.payment import Payment
from tests.utils import gen_random_hash


@pytest.fixture
def lightning_host_port():
    return LightningAddressHostPort(host="my_lightning_host", port=8765)


@pytest.fixture
def price_msat():
    return 777


@pytest.fixture
def nonce():
    return generate_tweak()


# @pytest.fixture
# def preimage():
#     # TODO: This should be generated from the tweak of the decryption key.
#     yield gen_random_hash()


@pytest.fixture
def preimage(secret_key, nonce):
    # TODO: This should be generated from the tweak of the decryption key.
    # yield gen_random_hash()
    # yield sha256(secret_key)
    yield add_tweak(secret_key, nonce)
    # yield add_tweak(secret_key, b'fooooo')
    # yield gen_random_hash()


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
def timestamp():
    yield 8888888


@pytest.fixture
def expiry():
    yield 5555


@pytest.fixture
def seller_pubkey():
    yield "fake_seller_pubkey"


@pytest.fixture
def uris():
    yield [
        'fake_pubkey@foobar.com:12345',
        'fake_pubkey@fakehost.com:56789',
    ]


@pytest.fixture
def info(uris):
    yield Info(
        uris=uris,
    )


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


@pytest.fixture
def pay_req(
        payment_hash,
        price_msat,
        payment_request,
        seller_pubkey,
        timestamp,
        expiry,
):
    yield PayReq(
        payment_hash=payment_hash,
        num_msat=price_msat,
        destination=seller_pubkey,
        timestamp=timestamp,
        expiry=expiry,
    )


@pytest.fixture
def successful_payment(preimage):
    yield Payment(
        payment_preimage=preimage,
        payment_error='',
    )


@pytest.fixture
def failed_payment(payment_request):
    yield Payment(
        payment_preimage=b'',
        payment_error='Payment failed.',
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

    def __init__(self, info, invoice, pay_req, payment):
        self.info = info
        self.invoice = invoice
        self.pay_req = pay_req
        self.payment = payment

    def get_info(self):
        return self.info

    def create_invoice(self, preimage: bytes, amount_msat: int):
        return self.invoice

    def decode_pay_req(self, payment_request: str):
        return self.pay_req

    def pay_invoice(self, payment_request: str):
        return self.payment

    def subscribe_invoices(self, settle_index: int):
        pass


@pytest.fixture
def bitcoin_client(genesis_block_info):
    return MockBitcoinClient(genesis_block_info)


@pytest.fixture
def lightning_client(info, invoice):
    return MockLightningClient(info, invoice, None, None)


@pytest.fixture
def buyer_lightning_client(pay_req, successful_payment):
    return MockLightningClient(None, None, pay_req, successful_payment)


@pytest.fixture
def squeak_core(bitcoin_client, lightning_client):
    yield SqueakCore(bitcoin_client, lightning_client)


@pytest.fixture
def buyer_squeak_core(bitcoin_client, buyer_lightning_client):
    yield SqueakCore(bitcoin_client, buyer_lightning_client)


# @pytest.fixture
# def squeak_and_decryption_key(squeak_core, signing_profile, squeak_content):
#     yield squeak_core.make_squeak(
#         signing_profile,
#         squeak_content,
#     )


# @pytest.fixture
# def squeak(squeak_and_decryption_key):
#     squeak, _ = squeak_and_decryption_key
#     yield squeak


# @pytest.fixture
# def decryption_key(squeak_and_decryption_key):
#     _, decryption_key = squeak_and_decryption_key
#     yield decryption_key


@pytest.fixture
def peer_address():
    yield PeerAddress(
        network=Network.IPV4,
        host="fake_host",
        port=8765,
    )


@pytest.fixture
def seller_peer_address():
    yield PeerAddress(
        network=Network.IPV4,
        host="fake_seller_host",
        port=4321,
    )


@pytest.fixture
def created_offer(squeak_core, squeak, secret_key, peer_address, price_msat):
    yield squeak_core.create_offer(
        squeak,
        secret_key,
        peer_address,
        price_msat,
    )


@pytest.fixture
def packaged_offer(squeak_core, created_offer):
    yield squeak_core.package_offer(created_offer, None)


@pytest.fixture
def unpacked_offer(buyer_squeak_core, squeak, packaged_offer, seller_peer_address):
    yield buyer_squeak_core.unpack_offer(squeak, packaged_offer, seller_peer_address)


@pytest.fixture
def sent_payment(buyer_squeak_core, unpacked_offer):
    yield buyer_squeak_core.pay_offer(unpacked_offer)


def test_get_block_header(
        squeak_core,
        squeak,
        genesis_block_info,
):
    block_header = squeak_core.get_block_header(squeak)

    assert block_header == genesis_block_info.block_header


# TODO: this is redundant with the other test.
# def test_get_decrypted_content(squeak_core, squeak, secret_key, squeak_content):
#     decrypted_content = squeak_core.get_decrypted_content(
#         squeak,
#         secret_key,
#     )

#     assert decrypted_content == squeak_content


def test_get_best_block_height(buyer_squeak_core, genesis_block_info):
    best_block_height = buyer_squeak_core.get_best_block_height()

    assert best_block_height == genesis_block_info.block_height


def test_create_offer(squeak, peer_address, price_msat, created_offer, invoice):

    assert created_offer.squeak_hash == get_hash(squeak)
    assert created_offer.payment_hash == invoice.r_hash
    # assert created_offer.secret_key == secret_key
    assert created_offer.price_msat == price_msat
    assert created_offer.payment_request == invoice.payment_request
    assert created_offer.invoice_time == invoice.creation_date
    assert created_offer.invoice_expiry == invoice.expiry
    assert created_offer.peer_address == peer_address


def test_packaged_offer(squeak, packaged_offer):

    assert packaged_offer is not None


def test_unpacked_offer(unpacked_offer):

    assert unpacked_offer is not None


def test_sent_payment(sent_payment):

    assert sent_payment is not None


# def test_unlock_squeak(squeak_core, squeak, squeak_content, sent_payment):
#     decrypted_content = squeak_core.get_decrypted_content(
#         squeak,
#         sent_payment.secret_key,
#     )

#     assert decrypted_content == squeak_content
