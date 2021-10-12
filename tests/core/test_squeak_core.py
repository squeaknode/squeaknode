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
from squeaknode.core.squeaks import make_squeak_with_block
from squeaknode.lightning.info import Info
from squeaknode.lightning.invoice import Invoice
from squeaknode.lightning.lightning_client import LightningClient
from squeaknode.lightning.pay_req import PayReq
from squeaknode.lightning.payment import Payment
from tests.utils import gen_random_hash
from tests.utils import sha256


@pytest.fixture
def lightning_host_port():
    return LightningAddressHostPort(host="my_lightning_host", port=8765)


@pytest.fixture
def price_msat():
    return 777


@pytest.fixture
def nonce():
    yield generate_tweak()


@pytest.fixture
def preimage(secret_key, nonce):
    yield add_tweak(secret_key, nonce)


@pytest.fixture
def payment_hash(preimage):
    # TODO: When PTLC is used, this should be the payment point of preimage.
    yield sha256(preimage)


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
def invoice(payment_request, price_msat, creation_date, expiry):
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
        payment_point=b'',
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


@pytest.fixture
def other_block_info():
    yield BlockInfo(
        block_height=5678,
        block_hash=gen_random_hash(),
        block_header=b'',
    )


@pytest.fixture
def other_squeak(signing_key, squeak_content, other_block_info):
    squeak, _ = make_squeak_with_block(
        signing_key,
        squeak_content,
        other_block_info.block_height,
        other_block_info.block_hash,
    )
    yield squeak


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
def lightning_client(info, invoice, pay_req, successful_payment):
    return MockLightningClient(info, invoice, pay_req, successful_payment)


@pytest.fixture
def squeak_core(bitcoin_client, lightning_client):
    yield SqueakCore(bitcoin_client, lightning_client)


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
def created_offer(squeak_core, squeak, secret_key, peer_address, price_msat, nonce):
    yield squeak_core.create_offer(
        squeak,
        secret_key,
        peer_address,
        price_msat,
        nonce,
    )


@pytest.fixture
def packaged_offer(squeak_core, created_offer):
    yield squeak_core.package_offer(created_offer, None)


@pytest.fixture
def unpacked_offer(squeak_core, squeak, packaged_offer, seller_peer_address):
    yield squeak_core.unpack_offer(
        squeak,
        packaged_offer,
        seller_peer_address,
    )


@pytest.fixture
def sent_payment(squeak_core, unpacked_offer):
    yield squeak_core.pay_offer(unpacked_offer)


def test_make_squeak(
        squeak_core,
        signing_profile,
        squeak_content,
):
    created_squeak, created_secret_key = squeak_core.make_squeak(
        signing_profile,
        squeak_content,
    )
    decrypted_created_content = squeak_core.get_decrypted_content(
        created_squeak,
        created_secret_key,
    )

    assert decrypted_created_content == squeak_content


def test_make_squeak_with_contact_profile(
        squeak_core,
        contact_profile,
        squeak_content,
):
    with pytest.raises(Exception):
        created_squeak, created_secret_key = squeak_core.make_squeak(
            contact_profile,
            squeak_content,
        )


def test_get_block_header(
        squeak_core,
        squeak,
        genesis_block_info,
):
    block_header = squeak_core.get_block_header(squeak)

    assert block_header == genesis_block_info.block_header


def test_get_block_header_invalid_block_hash(
        squeak_core,
        other_squeak,
):
    with pytest.raises(Exception):
        squeak_core.get_block_header(other_squeak)


def test_check_squeak(squeak_core, squeak):
    squeak_core.check_squeak(squeak)


def test_get_best_block_height(squeak_core, genesis_block_info):
    best_block_height = squeak_core.get_best_block_height()

    assert best_block_height == genesis_block_info.block_height


def test_create_offer(squeak, peer_address, price_msat, created_offer, invoice):

    assert created_offer.squeak_hash == get_hash(squeak)
    assert created_offer.payment_hash == invoice.r_hash
    assert created_offer.price_msat == price_msat
    assert created_offer.payment_request == invoice.payment_request
    assert created_offer.invoice_time == invoice.creation_date
    assert created_offer.invoice_expiry == invoice.expiry
    assert created_offer.peer_address == peer_address


def test_packaged_offer(squeak, packaged_offer):

    assert packaged_offer is not None


def test_unpacked_offer(unpacked_offer):

    assert unpacked_offer is not None


def test_unpacked_offer_bad_payment_point(squeak_core, squeak, packaged_offer, seller_peer_address):
    with pytest.raises(Exception):
        squeak_core.unpack_offer(
            squeak,
            packaged_offer,
            seller_peer_address,
            check_payment_point=True,
        )


def test_sent_payment(sent_payment):

    assert sent_payment is not None


def test_unlock_squeak(squeak_core, squeak, squeak_content, sent_payment):
    decrypted_content = squeak_core.get_decrypted_content(
        squeak,
        sent_payment.secret_key,
    )

    assert decrypted_content == squeak_content
