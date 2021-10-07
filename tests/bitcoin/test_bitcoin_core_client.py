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

from squeaknode.bitcoin.bitcoin_core_bitcoin_client import BitcoinCoreBitcoinClient
from squeaknode.bitcoin.exception import InvalidResultError
from squeaknode.bitcoin.exception import InvalidStatusError


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


class MockGetCountResponse:
    def json(self):
        return {'result': '555'}

    @property
    def status_code(self):
        return 200


class MockEmptyResponse:
    def json(self):
        return {}

    @property
    def status_code(self):
        return 200


class MockInvalidStatusResponse:
    def json(self):
        return {}

    @property
    def status_code(self):
        return 500


@pytest.fixture
def mock_get_count_response():
    yield MockGetCountResponse()


@pytest.fixture
def mock_empty_response():
    yield MockEmptyResponse()


@pytest.fixture
def mock_invalid_status_response():
    yield MockInvalidStatusResponse()


def test_get_block_count(bitcoin_core_client, mock_get_count_response):
    with mock.patch('squeaknode.bitcoin.bitcoin_core_bitcoin_client.requests.post', autospec=True) as mock_post:
        mock_post.return_value = mock_get_count_response
        block_count = bitcoin_core_client.get_block_count()

        assert block_count == 555


def test_get_block_count_no_result(bitcoin_core_client, mock_empty_response):
    with mock.patch('squeaknode.bitcoin.bitcoin_core_bitcoin_client.requests.post', autospec=True) as mock_post:
        mock_post.return_value = mock_empty_response

        with pytest.raises(InvalidResultError):
            bitcoin_core_client.get_block_count()


def test_get_block_count_invalid_status(bitcoin_core_client, mock_invalid_status_response):
    with mock.patch('squeaknode.bitcoin.bitcoin_core_bitcoin_client.requests.post', autospec=True) as mock_post:
        mock_post.return_value = mock_invalid_status_response

        with pytest.raises(InvalidStatusError):
            bitcoin_core_client.get_block_count()
