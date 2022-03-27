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

from squeaknode.core.lightning_address import LightningAddressHostPort
from squeaknode.db.squeak_db import SqueakDb
from squeaknode.node.squeak_store import SqueakStore


@pytest.fixture
def squeak_db():
    return mock.Mock(spec=SqueakDb)


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
def max_squeaks_per_public_key_per_block():
    return 10


@pytest.fixture
def squeak_retention_s():
    return 360000


@pytest.fixture
def received_offer_retention_s():
    return 3600


@pytest.fixture
def sent_offer_retention_s():
    return 7200


@pytest.fixture
def inserted_signing_profile_id(squeak_db, signing_profile):
    yield squeak_db.insert_profile(signing_profile)


@pytest.fixture
def squeak_store(
    squeak_db,
    max_squeaks,
    max_squeaks_per_public_key_per_block,
    squeak_retention_s,
    received_offer_retention_s,
    sent_offer_retention_s,
):
    return SqueakStore(
        squeak_db,
        max_squeaks,
        max_squeaks_per_public_key_per_block,
        squeak_retention_s,
        received_offer_retention_s,
        sent_offer_retention_s,
    )


def test_save_squeak(squeak_store, squeak_db, block_header, squeak, squeak_hash):
    with mock.patch.object(squeak_db, 'get_number_of_squeaks', autospec=True) as mock_get_number_of_squeaks, \
            mock.patch.object(squeak_db, 'number_of_squeaks_with_public_key_with_block_height', autospec=True) as mock_number_of_squeaks_with_public_key_with_block_height, \
            mock.patch.object(squeak_db, 'insert_squeak', autospec=True) as mock_insert_squeak, \
            mock.patch.object(squeak_store.new_squeak_listener, 'handle_new_item', autospec=True) as mock_handle_new_squeak:
        mock_get_number_of_squeaks.return_value = 0
        mock_number_of_squeaks_with_public_key_with_block_height.return_value = 0
        mock_insert_squeak.return_value = squeak_hash
        squeak_store.save_squeak(squeak, block_header)

        mock_insert_squeak.assert_called_once_with(squeak, block_header)
        mock_handle_new_squeak.assert_called_once_with(squeak)


def test_save_squeak_above_max(squeak_store, squeak_db, block_header, squeak, squeak_hash, max_squeaks):
    with mock.patch.object(squeak_db, 'get_number_of_squeaks', autospec=True) as mock_get_number_of_squeaks, \
            mock.patch.object(squeak_db, 'number_of_squeaks_with_public_key_with_block_height', autospec=True) as mock_number_of_squeaks_with_public_key_with_block_height, \
            mock.patch.object(squeak_db, 'insert_squeak', autospec=True) as mock_insert_squeak, \
            mock.patch.object(squeak_store.new_squeak_listener, 'handle_new_item', autospec=True) as mock_handle_new_squeak:
        mock_get_number_of_squeaks.return_value = max_squeaks + 1
        mock_number_of_squeaks_with_public_key_with_block_height.return_value = 0
        mock_insert_squeak.return_value = squeak_hash

        with pytest.raises(Exception):
            squeak_store.save_squeak(squeak)

        assert mock_insert_squeak.call_count == 0
        assert mock_handle_new_squeak.call_count == 0


def test_save_squeak_above_max_per_pubkey(squeak_store, squeak_db, block_header, squeak, squeak_hash, max_squeaks_per_public_key_per_block):
    with mock.patch.object(squeak_db, 'get_number_of_squeaks', autospec=True) as mock_get_number_of_squeaks, \
            mock.patch.object(squeak_db, 'number_of_squeaks_with_public_key_with_block_height', autospec=True) as mock_number_of_squeaks_with_public_key_with_block_height, \
            mock.patch.object(squeak_db, 'insert_squeak', autospec=True) as mock_insert_squeak, \
            mock.patch.object(squeak_store.new_squeak_listener, 'handle_new_item', autospec=True) as mock_handle_new_squeak:
        mock_get_number_of_squeaks.return_value = 0
        mock_number_of_squeaks_with_public_key_with_block_height.return_value = max_squeaks_per_public_key_per_block + 1
        mock_insert_squeak.return_value = squeak_hash

        with pytest.raises(Exception):
            squeak_store.save_squeak(squeak)

        assert mock_insert_squeak.call_count == 0
        assert mock_handle_new_squeak.call_count == 0


def test_save_secret_key(squeak_store, squeak_db, squeak, squeak_hash, secret_key):
    with mock.patch.object(squeak_db, 'get_squeak', autospec=True) as mock_get_squeak, \
            mock.patch.object(squeak_db, 'set_squeak_secret_key', autospec=True) as mock_set_squeak_secret_key, \
            mock.patch.object(squeak_store.new_secret_key_listener, 'handle_new_item', autospec=True) as mock_handle_new_secret_key:
        mock_get_squeak.return_value = squeak
        squeak_store.save_secret_key(squeak_hash, secret_key)

        mock_set_squeak_secret_key.assert_called_once_with(
            squeak_hash, secret_key)
        mock_handle_new_secret_key.assert_called_once_with(squeak)


# @pytest.fixture
# def unlocked_squeak(squeak_store, saved_squeak, secret_key, squeak_content):
#     saved_squeak_hash = get_hash(saved_squeak)
#     squeak_store.unlock_squeak(saved_squeak_hash, secret_key, squeak_content)
#     yield saved_squeak


# @pytest.fixture
# def deleted_squeak(squeak_store, unlocked_squeak):
#     unlocked_squeak_hash = get_hash(unlocked_squeak)
#     squeak_store.delete_squeak(unlocked_squeak_hash)
#     yield unlocked_squeak


# def test_get_squeak(squeak_store, saved_squeak):
#     saved_squeak_hash = get_hash(saved_squeak)
#     squeak_entry = squeak_store.get_squeak_entry(saved_squeak_hash)

#     assert saved_squeak == squeak_store.get_squeak(saved_squeak_hash)
#     assert squeak_entry.content is None
#     assert squeak_store.get_squeak_secret_key(saved_squeak_hash) is None


# def test_unlock_squeak(squeak_store, unlocked_squeak, squeak_content, secret_key):
#     unlocked_squeak_hash = get_hash(unlocked_squeak)
#     squeak_entry = squeak_store.get_squeak_entry(unlocked_squeak_hash)

#     assert unlocked_squeak == squeak_store.get_squeak(unlocked_squeak_hash)
#     assert squeak_entry.content == squeak_content
#     assert squeak_store.get_squeak_secret_key(
#         unlocked_squeak_hash) == secret_key


# def test_delete_squeak(squeak_store, deleted_squeak):
#     deleted_squeak_hash = get_hash(deleted_squeak)
#     squeak_entry = squeak_store.get_squeak_entry(deleted_squeak_hash)

#     assert squeak_store.get_squeak(deleted_squeak_hash) is None
#     assert squeak_entry is None
#     assert squeak_store.get_squeak_secret_key(deleted_squeak_hash) is None


def test_get_sent_offer_already_exists(squeak_store, squeak_db, sent_offer):
    with mock.patch.object(squeak_db, 'get_sent_offer_by_squeak_hash_and_peer', autospec=True) as mock_get_sent_offer_by_squeak_hash_and_peer:
        mock_get_sent_offer_by_squeak_hash_and_peer.return_value = sent_offer

        retrieved_sent_offer = squeak_store.get_sent_offer_by_squeak_hash_and_peer(
            sent_offer.squeak_hash,
            sent_offer.peer_address,
        )

    assert retrieved_sent_offer == sent_offer


def test_get_received_offer(squeak_store, squeak_db, received_offer):
    with mock.patch.object(
            squeak_db,
            'get_received_offer',
            new_callable=mock.PropertyMock,
    ) as mock_get_received_offer:
        mock_get_received_offer.return_value = received_offer

        retrieved_received_offer = squeak_store.get_received_offer(789)

    assert retrieved_received_offer == received_offer
    mock_get_received_offer.assert_called_once_with(789)
