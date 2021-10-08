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
from requests import HTTPError
from requests.exceptions import ConnectionError
from requests.exceptions import RequestException
from requests.exceptions import Timeout

from squeaknode.bitcoin.bitcoin_core_bitcoin_client import BitcoinCoreBitcoinClient
from squeaknode.bitcoin.exception import BitcoinConnectionError


@pytest.fixture
def bitcoin_core_client():
    yield BitcoinCoreBitcoinClient(
        host="fake_bitcoin_host",
        port=5678,
        rpc_user="fake_user",
        rpc_password="fake_pass",
        use_ssl=False,
        ssl_cert="fake_ssl_cert",
    )


@pytest.fixture
def block_count():
    yield 555


@pytest.fixture
def block_hash_str():
    yield '00000000edade40797e3c4bf27edeb65733d1884beaa8c502a89d50a54111e1c'


@pytest.fixture
def block_hash(block_hash_str):
    yield bytes.fromhex(block_hash_str)


@pytest.fixture
def block_header_str():
    yield '0100000079c30d2c23727a1e9f5feda4e7feb8ea0bda2ab98e23e7f6a9cf594f00000000b0de897e42fa7a3b5c3a6bfb8e797acf4ffbc16169394b03ad93296524ed633dcfef6e49ffff001d36d19a6c'


@pytest.fixture
def block_header(block_header_str):
    yield bytes.fromhex(block_header_str)


class MockResponse:

    def json(self):
        return {}

    @property
    def status_code(self):
        return 200

    def raise_for_status(self):
        pass


class MockGetCountResponse(MockResponse):

    def __init__(self, block_count):
        self.block_count = block_count

    def json(self):
        return {'result': '{}'.format(self.block_count)}


class MockGetBlockHashResponse(MockResponse):

    def __init__(self, block_hash_str):
        self.block_hash_str = block_hash_str

    def json(self):
        return {'result': '{}'.format(self.block_hash_str)}


class MockGetBlockHeaderResponse(MockResponse):

    def __init__(self, block_header_str):
        self.block_header_str = block_header_str

    def json(self):
        return {'result': '{}'.format(self.block_header_str)}


class MockEmptyResponse(MockResponse):
    def json(self):
        return {}


class MockInvalidStatusResponse(MockResponse):

    def raise_for_status(self):
        raise HTTPError("Some http error", response=self)


@pytest.fixture
def mock_get_count_response(block_count):
    yield MockGetCountResponse(block_count)


@pytest.fixture
def mock_get_block_hash_response(block_hash_str):
    yield MockGetBlockHashResponse(block_hash_str)


@pytest.fixture
def mock_get_block_header_response(block_header_str):
    yield MockGetBlockHeaderResponse(block_header_str)


@pytest.fixture
def mock_empty_response():
    yield MockEmptyResponse()


@pytest.fixture
def mock_invalid_status_response():
    yield MockInvalidStatusResponse()


def test_get_block_count(bitcoin_core_client, mock_get_count_response, block_count):
    with mock.patch('squeaknode.bitcoin.bitcoin_core_bitcoin_client.requests.post', autospec=True) as mock_post:
        mock_post.return_value = mock_get_count_response
        retrieved_block_count = bitcoin_core_client.get_block_count()

        assert retrieved_block_count == block_count


def test_get_block_count_invalid_status(bitcoin_core_client, mock_invalid_status_response):
    with mock.patch('squeaknode.bitcoin.bitcoin_core_bitcoin_client.requests.post', autospec=True) as mock_post:
        mock_post.return_value = mock_invalid_status_response

        with pytest.raises(BitcoinConnectionError):
            bitcoin_core_client.get_block_count()


def test_get_block_count_connection_error(bitcoin_core_client, mock_invalid_status_response):
    with mock.patch('squeaknode.bitcoin.bitcoin_core_bitcoin_client.requests.post', autospec=True) as mock_post:
        mock_post.side_effect = ConnectionError()

        with pytest.raises(BitcoinConnectionError):
            bitcoin_core_client.get_block_count()


def test_get_block_count_timeout_error(bitcoin_core_client, mock_invalid_status_response):
    with mock.patch('squeaknode.bitcoin.bitcoin_core_bitcoin_client.requests.post', autospec=True) as mock_post:
        mock_post.side_effect = Timeout()

        with pytest.raises(BitcoinConnectionError):
            bitcoin_core_client.get_block_count()


def test_get_block_count_request_exception(bitcoin_core_client, mock_invalid_status_response):
    with mock.patch('squeaknode.bitcoin.bitcoin_core_bitcoin_client.requests.post', autospec=True) as mock_post:
        mock_post.side_effect = RequestException()

        with pytest.raises(BitcoinConnectionError):
            bitcoin_core_client.get_block_count()


def test_get_block_hash(bitcoin_core_client, mock_get_block_hash_response, block_count, block_hash):
    with mock.patch('squeaknode.bitcoin.bitcoin_core_bitcoin_client.requests.post', autospec=True) as mock_post:
        mock_post.return_value = mock_get_block_hash_response
        retrieved_block_hash = bitcoin_core_client.get_block_hash(block_count)

        assert retrieved_block_hash == block_hash


def test_get_block_header(bitcoin_core_client, mock_get_block_header_response, block_hash, block_header):
    with mock.patch('squeaknode.bitcoin.bitcoin_core_bitcoin_client.requests.post', autospec=True) as mock_post:
        mock_post.return_value = mock_get_block_header_response
        retrieved_block_header = bitcoin_core_client.get_block_header(
            block_hash)

        assert retrieved_block_header == block_header
