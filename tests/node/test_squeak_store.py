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
from squeaknode.core.squeaks import get_hash
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
def inserted_signing_profile_id(squeak_db, signing_profile):
    yield squeak_db.insert_profile(signing_profile)


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


@pytest.fixture
def saved_squeak(squeak_store, squeak_core, block_header, squeak):
    with mock.patch.object(squeak_core, 'get_block_header', autospec=True) as mock_get_block_header:
        mock_get_block_header.return_value = block_header
        squeak_store.save_squeak(squeak)
        yield squeak


@pytest.fixture
def unlocked_squeak(squeak_store, squeak_core, saved_squeak, secret_key, squeak_content):
    with mock.patch.object(squeak_core, 'get_decrypted_content', autospec=True) as mock_get_decrypted_content:
        mock_get_decrypted_content.return_value = squeak_content
        saved_squeak_hash = get_hash(saved_squeak)
        squeak_store.unlock_squeak(saved_squeak_hash, secret_key)
        yield saved_squeak


@pytest.fixture
def deleted_squeak(squeak_store, unlocked_squeak):
    unlocked_squeak_hash = get_hash(unlocked_squeak)
    squeak_store.delete_squeak(unlocked_squeak_hash)
    yield unlocked_squeak


def test_get_squeak(squeak_store, saved_squeak):
    saved_squeak_hash = get_hash(saved_squeak)
    squeak_entry = squeak_store.get_squeak_entry(saved_squeak_hash)

    assert saved_squeak == squeak_store.get_squeak(saved_squeak_hash)
    assert squeak_entry.content is None
    assert squeak_store.get_squeak_secret_key(saved_squeak_hash) is None


def test_unlock_squeak(squeak_store, unlocked_squeak, squeak_content, secret_key):
    unlocked_squeak_hash = get_hash(unlocked_squeak)
    squeak_entry = squeak_store.get_squeak_entry(unlocked_squeak_hash)

    assert unlocked_squeak == squeak_store.get_squeak(unlocked_squeak_hash)
    assert squeak_entry.content == squeak_content
    assert squeak_store.get_squeak_secret_key(
        unlocked_squeak_hash) == secret_key


def test_delete_squeak(squeak_store, deleted_squeak):
    deleted_squeak_hash = get_hash(deleted_squeak)
    squeak_entry = squeak_store.get_squeak_entry(deleted_squeak_hash)

    assert squeak_store.get_squeak(deleted_squeak_hash) is None
    assert squeak_entry is None
    assert squeak_store.get_squeak_secret_key(deleted_squeak_hash) is None


def test_make_squeak(
        squeak_store,
        squeak_core,
        block_header,
        squeak,
        squeak_hash,
        secret_key,
        squeak_content,
        inserted_signing_profile_id,
):
    with mock.patch.object(squeak_core, 'make_squeak', autospec=True) as mock_make_squeak, \
            mock.patch.object(squeak_core, 'get_block_header', autospec=True) as mock_get_block_header, \
            mock.patch.object(squeak_core, 'get_decrypted_content', autospec=True) as mock_get_decrypted_content:
        mock_make_squeak.return_value = squeak, secret_key
        mock_get_block_header.return_value = block_header
        mock_get_decrypted_content.return_value = squeak_content
        squeak_store.make_squeak(
            inserted_signing_profile_id, squeak_content, None)

    squeak_entry = squeak_store.get_squeak_entry(squeak_hash)

    assert squeak == squeak_store.get_squeak(squeak_hash)
    assert squeak_entry.content == squeak_content


@pytest.fixture
def test_get_free_secret_key(squeak_store, squeak_core, unlocked_squeak, secret_key, peer_address):
    unlocked_squeak_hash = get_hash(unlocked_squeak)
    secret_key_reply = squeak_store.get_secret_key_reply(
        unlocked_squeak_hash, peer_address, 0, None)

    assert secret_key_reply.squeak_hash == unlocked_squeak_hash
    assert secret_key.secret_key == secret_key
