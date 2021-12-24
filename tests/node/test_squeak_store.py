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
from squeaknode.core.squeaks import get_hash
from squeaknode.db.squeak_db import SqueakDb
from squeaknode.node.squeak_store import SqueakStore


@pytest.fixture
def db_engine():
    yield create_engine('sqlite://')


@pytest.fixture
def squeak_db(db_engine):
    # TODO: use a mock object for db.
    db = SqueakDb(db_engine)
    db.init()
    yield db


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
def inserted_signing_profile_id(squeak_db, signing_profile):
    yield squeak_db.insert_profile(signing_profile)


# @pytest.fixture
# def inserted_received_offer_id(squeak_db, received_offer, creation_date):
#     with mock.patch.object(SqueakDb, 'timestamp_now_ms', new_callable=mock.PropertyMock) as mock_timestamp_ms:
#         mock_timestamp_ms.return_value = creation_date / 1000
#         yield squeak_db.insert_received_offer(received_offer)


@pytest.fixture
def squeak_store(
    squeak_db,
    max_squeaks,
    max_squeaks_per_public_key_per_block,
):
    return SqueakStore(
        squeak_db,
        max_squeaks,
        max_squeaks_per_public_key_per_block,
    )


@pytest.fixture
def saved_squeak(squeak_store, block_header, squeak):
    squeak_store.save_squeak(squeak, block_header)
    yield squeak


@pytest.fixture
def unlocked_squeak(squeak_store, saved_squeak, secret_key, squeak_content):
    saved_squeak_hash = get_hash(saved_squeak)
    squeak_store.unlock_squeak(saved_squeak_hash, secret_key, squeak_content)
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


def test_save_sent_offer(squeak_store, squeak_db, sent_offer):
    with mock.patch.object(
            squeak_db,
            'insert_sent_offer',
            new_callable=mock.PropertyMock,
    ) as mock_insert_sent_offer:
        mock_insert_sent_offer.return_value = 555

        inserted_sent_offer_id = squeak_store.save_sent_offer(sent_offer)

    assert inserted_sent_offer_id == 555
    print("mock_insert_sent_offer.call_count:")
    print(mock_insert_sent_offer.call_count)
    mock_insert_sent_offer.assert_called_once_with(sent_offer)


def test_get_sent_offer(squeak_store, squeak_db, sent_offer):
    with mock.patch.object(
            squeak_db,
            'get_sent_offer_by_squeak_hash_and_peer',
            new_callable=mock.PropertyMock,
    ) as mock_get_sent_offer_by_squeak_hash_and_peer:
        mock_get_sent_offer_by_squeak_hash_and_peer.return_value = sent_offer

        retrieved_sent_offer = squeak_store.get_sent_offer_for_peer(
            sent_offer.squeak_hash, sent_offer.peer_address)

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


# def test_get_free_secret_key(squeak_store, squeak_core, unlocked_squeak, secret_key, peer_address):
#     unlocked_squeak_hash = get_hash(unlocked_squeak)
#     secret_key_reply = squeak_store.get_secret_key_reply(
#         unlocked_squeak_hash, peer_address, 0, None)

#     assert secret_key_reply.squeak_hash == unlocked_squeak_hash
#     assert secret_key_reply.secret_key == secret_key


# def test_get_offer_secret_key(squeak_store, squeak_core, unlocked_squeak, secret_key, peer_address, sent_offer, offer):
#     with mock.patch.object(squeak_core, 'create_offer', autospec=True) as mock_create_offer, \
#             mock.patch.object(squeak_core, 'package_offer', autospec=True) as mock_package_offer:
#         mock_create_offer.return_value = sent_offer
#         mock_package_offer.return_value = offer
#         unlocked_squeak_hash = get_hash(unlocked_squeak)
#         secret_key_reply = squeak_store.get_secret_key_reply(
#             unlocked_squeak_hash, peer_address, 1000, None)

#     assert secret_key_reply.squeak_hash == unlocked_squeak_hash
#     assert secret_key_reply.offer == offer


# def test_pay_offer(
#         squeak_store,
#         squeak_db,
#         squeak_core,
#         unlocked_squeak,
#         block_header,
#         squeak_content,
#         secret_key,
#         peer_address,
#         inserted_received_offer_id,
#         sent_payment,
# ):
#     with mock.patch.object(squeak_core, 'pay_offer', autospec=True) as mock_pay_offer, \
#             mock.patch.object(squeak_core, 'get_block_header', autospec=True) as mock_get_block_header, \
#             mock.patch.object(squeak_core, 'get_decrypted_content', autospec=True) as mock_get_decrypted_content:
#         mock_pay_offer.return_value = sent_payment
#         mock_get_block_header.return_value = block_header
#         mock_get_decrypted_content.return_value = squeak_content
#         sent_payment_id = squeak_store.pay_offer(inserted_received_offer_id)

#     retrieved_sent_payment = squeak_db.get_sent_payment(
#         sent_payment_id,
#     )

#     assert sent_payment_id is not None
#     assert retrieved_sent_payment is not None


# def test_save_received_offer_already_unlocked(
#         squeak_store,
#         unlocked_squeak,
#         offer,
#         peer_address,
# ):
#     received_offer_id = squeak_store.save_received_offer(
#         offer,
#         peer_address,
#     )

#     assert received_offer_id is None


# def test_save_received_offer(
#         squeak_store,
#         squeak_db,
#         squeak_core,
#         saved_squeak,
#         offer,
#         received_offer,
#         peer_address,
# ):
#     with mock.patch.object(squeak_core, 'unpack_offer', autospec=True) as mock_unpack_offer:
#         mock_unpack_offer.return_value = received_offer
#         received_offer_id = squeak_store.save_received_offer(
#             offer,
#             peer_address,
#         )

#     assert received_offer_id is not None
#     retrieved_received_offer = squeak_db.get_received_offer(received_offer_id)

#     assert retrieved_received_offer == received_offer._replace(
#         received_offer_id=received_offer_id,
#     )