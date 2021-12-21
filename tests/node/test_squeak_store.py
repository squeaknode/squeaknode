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
from sqlalchemy import create_engine

from squeaknode.core.lightning_address import LightningAddressHostPort
from squeaknode.core.squeak_core import SqueakCore
from squeaknode.db.squeak_db import SqueakDb
from squeaknode.node.squeak_store import SqueakStore


@pytest.fixture
def db_engine():
    yield create_engine('sqlite://')


@pytest.fixture
def squeak_db(db_engine):
    db = SqueakDb(db_engine)
    db.init()
    yield db


@pytest.fixture
def squeak_core():
    return mock.Mock(spec=SqueakCore)


@pytest.fixture
def lightning_host_port():
    return LightningAddressHostPort(host="my_lightning_host", port=8765)


@pytest.fixture
def price_msat():
    return 777


@pytest.fixture
def max_squeaks():
    return 55


@pytest.fixture
def max_squeaks_per_public_key_in_block_range():
    return 10


@pytest.fixture
def squeak_store(
    squeak_db,
    squeak_core,
    max_squeaks,
    max_squeaks_per_public_key_in_block_range,
):
    return SqueakStore(
        squeak_db,
        squeak_core,
        max_squeaks,
        max_squeaks_per_public_key_in_block_range,
    )


def test_save_squeak(squeak_store, squeak_core, block_header, squeak, squeak_hash):
    with mock.patch.object(squeak_core, 'get_block_header', autospec=True) as mock_get_block_header:
        mock_get_block_header.return_value = block_header
        squeak_store.save_squeak(squeak)

    assert squeak == squeak_store.get_squeak(squeak_hash)


def test_unlock_squeak(squeak_store, squeak_core, block_header, squeak, squeak_hash, secret_key, squeak_content):
    with mock.patch.object(squeak_core, 'get_block_header', autospec=True) as mock_get_block_header, \
            mock.patch.object(squeak_core, 'get_decrypted_content', autospec=True) as mock_get_decrypted_content:
        mock_get_block_header.return_value = block_header
        mock_get_decrypted_content.return_value = squeak_content
        squeak_store.save_squeak(squeak)

        squeak_store.unlock_squeak(squeak_hash, secret_key)

    squeak_entry = squeak_store.get_squeak_entry(squeak_hash)

    assert squeak_entry.content == squeak_content
