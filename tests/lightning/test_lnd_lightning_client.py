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

from proto import lnd_pb2
from squeaknode.lightning.lnd_lightning_client import LNDLightningClient
from tests.utils import gen_random_hash


@pytest.fixture
def lnd_host():
    yield "fake_lnd_host"


@pytest.fixture
def lnd_port():
    yield 9876


@pytest.fixture
def tls_cert_path():
    yield "fake_tls_cert_path"


@pytest.fixture
def macaroon_path():
    yield "fake_macaroon_path"


@pytest.fixture
def preimage():
    yield gen_random_hash()


@pytest.fixture
def price_msat():
    yield 33333


@pytest.fixture
def rpc_invoice(preimage):
    yield lnd_pb2.Invoice(
        memo='hello',
        r_preimage=preimage,
    )


# @pytest.fixture
# def lnd_lightning_client_and_get_stub(lnd_host, lnd_port, tls_cert_path, macaroon_path):
#     client = LNDLightningClient(
#         host=lnd_host,
#         port=lnd_port,
#         tls_cert_path=tls_cert_path,
#         macaroon_path=macaroon_path,
#     )
#     with mock.patch.object(client, '_get_stub', autospec=True) as mock_get_stub:
#         yield client, mock_get_stub


# @pytest.fixture
# def lnd_lightning_client(lnd_lightning_client_and_get_stub):
#     client, _ = lnd_lightning_client_and_get_stub
#     yield client


# @pytest.fixture
# def mock_get_stub(lnd_lightning_client_and_get_stub):
#     _, get_stub = lnd_lightning_client_and_get_stub
#     yield get_stub


@pytest.fixture
def make_lightning_client(lnd_host, lnd_port, tls_cert_path, macaroon_path):
    client = LNDLightningClient(
        host=lnd_host,
        port=lnd_port,
        tls_cert_path=tls_cert_path,
        macaroon_path=macaroon_path,
    )
    with mock.patch.object(client, '_get_stub', autospec=True) as mock_get_stub:
        def fn(stub):
            mock_get_stub.return_value = stub
            client.init()
            return client
        yield fn


def test_add_invoice(make_lightning_client, preimage, price_msat, rpc_invoice):
    mock_stub = mock.MagicMock()
    mock_stub.AddInvoice.return_value = rpc_invoice
    client = make_lightning_client(mock_stub)
    add_invoice_response = client.add_invoice(
        preimage, price_msat)
    (call_invoice,) = mock_stub.AddInvoice.call_args.args
    print(call_invoice)

    assert call_invoice.r_preimage == preimage
    assert call_invoice.value_msat == price_msat
    assert add_invoice_response == rpc_invoice
