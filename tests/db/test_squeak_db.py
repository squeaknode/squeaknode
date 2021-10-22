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
import time

import mock
import pytest
from sqlalchemy import create_engine

from squeaknode.db.squeak_db import SqueakDb
from tests.utils import gen_address
from tests.utils import gen_contact_profile
from tests.utils import gen_random_hash
from tests.utils import gen_signing_key
from tests.utils import gen_signing_profile
from tests.utils import gen_squeak_peer
from tests.utils import gen_squeak_with_block_header


@pytest.fixture
def db_engine():
    yield create_engine('sqlite://')


@pytest.fixture
def squeak_db(db_engine):
    db = SqueakDb(db_engine)
    db.init()
    yield db


@pytest.fixture
def inserted_squeak_hash(squeak_db, squeak, block_header):
    yield squeak_db.insert_squeak(squeak, block_header)


@pytest.fixture
def inserted_reply_squeak_hash(squeak_db, reply_squeak, block_header):
    yield squeak_db.insert_squeak(reply_squeak, block_header)


@pytest.fixture
def unlocked_squeak_hash(squeak_db, squeak, inserted_squeak_hash, secret_key, squeak_content):
    squeak_db.set_squeak_decryption_key(
        inserted_squeak_hash, secret_key, squeak_content)
    yield inserted_squeak_hash


@pytest.fixture
def deleted_squeak_hash(squeak_db, squeak_hash):
    squeak_db.delete_squeak(
        squeak_hash,
    )
    yield squeak_hash


@pytest.fixture
def inserted_signing_profile_id(squeak_db, signing_profile):
    yield squeak_db.insert_profile(signing_profile)


@pytest.fixture
def inserted_contact_profile_id(squeak_db, contact_profile):
    yield squeak_db.insert_profile(contact_profile)


@pytest.fixture
def inserted_contact_profile(squeak_db, inserted_contact_profile_id):
    yield squeak_db.get_profile(inserted_contact_profile_id)


@pytest.fixture
def followed_contact_profile_id(squeak_db, inserted_contact_profile_id):
    squeak_db.set_profile_following(
        inserted_contact_profile_id,
        True,
    )
    yield inserted_contact_profile_id


@pytest.fixture
def unfollowed_contact_profile_id(squeak_db, followed_contact_profile_id):
    squeak_db.set_profile_following(
        followed_contact_profile_id,
        False,
    )
    yield followed_contact_profile_id


@pytest.fixture
def profile_with_use_custom_price_id(squeak_db, inserted_contact_profile_id):
    squeak_db.set_profile_use_custom_price(
        inserted_contact_profile_id,
        True,
    )
    yield inserted_contact_profile_id


@pytest.fixture
def custom_price_msat():
    yield 502379


@pytest.fixture
def new_profile_name():
    yield "new_fake_profile_name"


@pytest.fixture
def profile_image_bytes():
    yield bytes.fromhex("deadbeef")


@pytest.fixture
def profile_with_custom_price_id(squeak_db, inserted_contact_profile_id, custom_price_msat):
    squeak_db.set_profile_custom_price_msat(
        inserted_contact_profile_id,
        custom_price_msat,
    )
    yield inserted_contact_profile_id


@pytest.fixture
def profile_with_new_name_id(squeak_db, inserted_contact_profile_id, new_profile_name):
    squeak_db.set_profile_name(
        inserted_contact_profile_id,
        new_profile_name,
    )
    yield inserted_contact_profile_id


@pytest.fixture
def profile_with_image_id(squeak_db, inserted_contact_profile_id, profile_image_bytes):
    squeak_db.set_profile_image(
        inserted_contact_profile_id,
        profile_image_bytes,
    )
    yield inserted_contact_profile_id


@pytest.fixture
def deleted_profile_id(squeak_db, inserted_contact_profile_id):
    squeak_db.delete_profile(
        inserted_contact_profile_id,
    )
    yield inserted_contact_profile_id


@pytest.fixture
def inserted_squeak_hashes(squeak_db, signing_key):
    ret = []
    for i in range(100):
        squeak, header = gen_squeak_with_block_header(signing_key, i)
        squeak_hash = squeak_db.insert_squeak(squeak, header)
        ret.append(squeak_hash)
    yield ret


@pytest.fixture
def followed_squeak_hashes(
        squeak_db,
        inserted_squeak_hashes,
        followed_contact_profile_id,
):
    yield inserted_squeak_hashes


@pytest.fixture
def authored_squeak_hashes(
        squeak_db,
        inserted_squeak_hashes,
        inserted_signing_profile_id,
):
    yield inserted_squeak_hashes


@pytest.fixture
def unfollowed_squeak_hashes(
        squeak_db,
        inserted_squeak_hashes,
        unfollowed_contact_profile_id,
):
    yield inserted_squeak_hashes


@pytest.fixture
def liked_squeak_hashes(squeak_db, inserted_squeak_hashes):
    for squeak_hash in inserted_squeak_hashes:
        squeak_db.set_squeak_liked(squeak_hash)
    yield inserted_squeak_hashes


@pytest.fixture
def unliked_squeak_hashes(squeak_db, liked_squeak_hashes):
    for squeak_hash in liked_squeak_hashes:
        squeak_db.set_squeak_unliked(squeak_hash)
    yield liked_squeak_hashes


@pytest.fixture
def liked_squeak_hash(squeak_db, inserted_squeak_hash):
    squeak_db.set_squeak_liked(inserted_squeak_hash)
    yield inserted_squeak_hash


@pytest.fixture
def unliked_squeak_hash(squeak_db, liked_squeak_hash):
    squeak_db.set_squeak_unliked(liked_squeak_hash)
    yield liked_squeak_hash


@pytest.fixture
def inserted_peer_id(squeak_db, peer):
    yield squeak_db.insert_peer(peer)


@pytest.fixture
def inserted_contact_profile_ids(squeak_db):
    ret = []
    for i in range(100):
        profile_name = "contact_profile_{}".format(i)
        address = str(gen_address())
        profile = gen_contact_profile(profile_name, address)
        profile_id = squeak_db.insert_profile(profile)
        ret.append(profile_id)
    yield ret


@pytest.fixture
def inserted_signing_profile_ids(squeak_db):
    ret = []
    for i in range(100):
        profile_name = "signing_profile_{}".format(i)
        signing_key = str(gen_signing_key())
        profile = gen_signing_profile(profile_name, signing_key)
        profile_id = squeak_db.insert_profile(profile)
        ret.append(profile_id)
    yield ret


@pytest.fixture
def followed_contact_profile_ids(squeak_db, inserted_contact_profile_ids):
    for profile_id in inserted_contact_profile_ids:
        squeak_db.set_profile_following(
            profile_id,
            True,
        )
    yield inserted_contact_profile_ids


@pytest.fixture
def inserted_squeak_peer_ids(squeak_db):
    ret = []
    for i in range(100):
        peer_name = "peer_{}".format(i)
        peer = gen_squeak_peer(peer_name)
        peer_id = squeak_db.insert_peer(peer)
        ret.append(peer_id)
    yield ret


@pytest.fixture
def autoconnect_squeak_peer_ids(squeak_db, inserted_squeak_peer_ids):
    for peer_id in inserted_squeak_peer_ids:
        squeak_db.set_peer_autoconnect(peer_id, True)
    yield inserted_squeak_peer_ids


@pytest.fixture
def new_peer_name():
    yield "new_fake_peer_name"


@pytest.fixture
def peer_with_new_name_id(squeak_db, inserted_peer_id, new_peer_name):
    squeak_db.set_peer_name(
        inserted_peer_id,
        new_peer_name,
    )
    yield inserted_peer_id


@pytest.fixture
def deleted_peer_id(squeak_db, inserted_peer_id):
    squeak_db.delete_peer(
        inserted_peer_id,
    )
    yield inserted_peer_id


@pytest.fixture
def inserted_received_offer_id(squeak_db, received_offer):
    yield squeak_db.insert_received_offer(received_offer)


@pytest.fixture
def duplicate_inserted_received_offer_id(squeak_db, inserted_received_offer_id, received_offer):
    yield squeak_db.insert_received_offer(received_offer)


def test_init_with_retries(squeak_db):
    with mock.patch.object(squeak_db, 'init', autospec=True) as mock_init, \
            mock.patch('squeaknode.db.squeak_db.time.sleep', autospec=True) as mock_sleep:
        ret = squeak_db.init_with_retries(num_retries=5, retry_interval_s=100)

        assert ret is None
        mock_init.assert_called_once_with()
        assert mock_sleep.call_count == 0


def test_init_with_retries_fail_once(squeak_db):
    with mock.patch.object(squeak_db, 'init', autospec=True) as mock_init, \
            mock.patch('squeaknode.db.squeak_db.time.sleep', autospec=True) as mock_sleep:
        mock_init.side_effect = [Exception('some db error'), None]
        ret = squeak_db.init_with_retries(num_retries=5, retry_interval_s=100)

        assert ret is None
        mock_init.call_count == 2
        assert mock_sleep.call_count == 1


def test_init_with_retries_fail_many_times(squeak_db):
    with mock.patch.object(squeak_db, 'init', autospec=True) as mock_init, \
            mock.patch('squeaknode.db.squeak_db.time.sleep', autospec=True) as mock_sleep:
        mock_init.side_effect = [Exception('some db error')] * 5

        with pytest.raises(Exception) as excinfo:
            squeak_db.init_with_retries(num_retries=5, retry_interval_s=100)
        assert "Failed to initialize database." in str(excinfo.value)

        mock_init.call_count == 5
        assert mock_sleep.call_count == 4


def test_get_squeak(squeak_db, squeak, inserted_squeak_hash):
    retrieved_squeak = squeak_db.get_squeak(inserted_squeak_hash)

    assert retrieved_squeak == squeak


def test_get_deleted_squeak(squeak_db, deleted_squeak_hash):
    retrieved_squeak = squeak_db.get_squeak(deleted_squeak_hash)

    assert retrieved_squeak is None


def test_insert_duplicate_squeak(squeak_db, squeak, block_header, inserted_squeak_hash):
    insert_result = squeak_db.insert_squeak(squeak, block_header)

    assert insert_result is None


def test_get_missing_squeak(squeak_db, squeak, squeak_hash):
    retrieved_squeak = squeak_db.get_squeak(squeak_hash)

    assert retrieved_squeak is None


def test_get_squeak_entry(squeak_db, squeak, block_header, address_str, inserted_squeak_hash):
    retrieved_squeak_entry = squeak_db.get_squeak_entry(inserted_squeak_hash)

    assert retrieved_squeak_entry.squeak_hash == inserted_squeak_hash
    assert retrieved_squeak_entry.address == address_str
    assert retrieved_squeak_entry.content is None
    assert retrieved_squeak_entry.block_time == block_header.nTime


def test_get_missing_squeak_entry(squeak_db, squeak, squeak_hash):
    retrieved_squeak_entry = squeak_db.get_squeak_entry(squeak_hash)

    assert retrieved_squeak_entry is None


def test_get_squeak_secret_key_and_content(
        squeak_db,
        squeak,
        secret_key,
        squeak_content,
        unlocked_squeak_hash,
):
    retrieved_squeak_entry = squeak_db.get_squeak_entry(unlocked_squeak_hash)
    retrieved_secret_key = squeak_db.get_squeak_secret_key(
        unlocked_squeak_hash,
    )

    assert retrieved_squeak_entry.squeak_hash == unlocked_squeak_hash
    assert retrieved_squeak_entry.content == squeak_content
    assert retrieved_secret_key == secret_key


def test_get_squeak_secret_key_and_content_locked(
        squeak_db,
        squeak,
        secret_key,
        squeak_content,
        inserted_squeak_hash,
):
    retrieved_squeak_entry = squeak_db.get_squeak_entry(inserted_squeak_hash)
    retrieved_secret_key = squeak_db.get_squeak_secret_key(
        inserted_squeak_hash,
    )

    assert retrieved_squeak_entry.squeak_hash == inserted_squeak_hash
    assert retrieved_squeak_entry.content is None
    assert retrieved_secret_key is None


def test_get_secret_key_missing_squeak(squeak_db, squeak, squeak_hash):
    retrieved_secret_key = squeak_db.get_squeak_secret_key(
        squeak_hash,
    )

    assert retrieved_secret_key is None


def test_get_timeline_squeak_entries(squeak_db, followed_squeak_hashes):
    timeline_squeak_entries = squeak_db.get_timeline_squeak_entries(
        limit=2,
        last_entry=None,
    )

    assert len(timeline_squeak_entries) == 2


def test_get_timeline_squeak_entries_all_unfollowed(squeak_db, unfollowed_squeak_hashes):
    timeline_squeak_entries = squeak_db.get_timeline_squeak_entries(
        limit=2,
        last_entry=None,
    )

    assert len(timeline_squeak_entries) == 0


def test_set_profile_following(squeak_db, followed_contact_profile_id):
    profile = squeak_db.get_profile(followed_contact_profile_id)

    assert profile.following


def test_set_profile_unfollowing(squeak_db, unfollowed_contact_profile_id):
    profile = squeak_db.get_profile(unfollowed_contact_profile_id)

    assert not profile.following


def test_set_profile_use_custom_price(squeak_db, profile_with_use_custom_price_id):
    profile = squeak_db.get_profile(profile_with_use_custom_price_id)

    assert profile.use_custom_price


def test_set_profile_custom_price(squeak_db, profile_with_custom_price_id, custom_price_msat):
    profile = squeak_db.get_profile(profile_with_custom_price_id)

    assert profile.custom_price_msat == custom_price_msat


def test_set_profile_name(squeak_db, profile_with_new_name_id, new_profile_name):
    profile = squeak_db.get_profile(profile_with_new_name_id)

    assert profile.profile_name == new_profile_name


def test_set_profile_image(squeak_db, profile_with_image_id, profile_image_bytes):
    profile = squeak_db.get_profile(profile_with_image_id)

    assert profile.profile_image == profile_image_bytes


def test_deleted_profile(squeak_db, deleted_profile_id):
    profile = squeak_db.get_profile(deleted_profile_id)

    assert profile is None


def test_get_liked_squeak_entries(
        squeak_db,
        liked_squeak_hashes,
):
    # Get the liked squeak entries.
    liked_squeak_entries = squeak_db.get_liked_squeak_entries(
        limit=200,
        last_entry=None,
    )

    assert len(liked_squeak_entries) == 100


def test_get_unliked_squeak_entries(
        squeak_db,
        unliked_squeak_hashes,
):
    # Get the liked squeak entries.
    liked_squeak_entries = squeak_db.get_liked_squeak_entries(
        limit=200,
        last_entry=None,
    )

    assert len(liked_squeak_entries) == 0


def test_set_squeak_liked(squeak_db, liked_squeak_hash):
    retrieved_squeak_entry = squeak_db.get_squeak_entry(liked_squeak_hash)

    assert retrieved_squeak_entry.liked_time_ms is not None


def test_set_squeak_unliked(squeak_db, unliked_squeak_hash):
    retrieved_squeak_entry = squeak_db.get_squeak_entry(unliked_squeak_hash)

    assert retrieved_squeak_entry.liked_time_ms is None


def test_get_peer(squeak_db, peer, inserted_peer_id):
    retrieved_peer = squeak_db.get_peer(inserted_peer_id)

    assert retrieved_peer._replace(peer_id=None) == peer


def test_get_peer_missing(squeak_db):
    retrieved_peer = squeak_db.get_peer(9876)

    assert retrieved_peer is None


def test_get_peer_by_address(squeak_db, peer, inserted_peer_id, peer_address):
    retrieved_peer = squeak_db.get_peer_by_address(peer_address)

    assert retrieved_peer._replace(peer_id=None) == peer


def test_get_peer_by_address_missing(squeak_db, peer, inserted_peer_id, peer_address):
    other_address = peer_address._replace(host="other_fake_host")
    retrieved_peer = squeak_db.get_peer_by_address(other_address)

    assert retrieved_peer is None


def test_get_address_squeak_entries(
        squeak_db,
        address_str,
        inserted_squeak_hashes,
):
    # Get the address squeak entries.
    address_squeak_entries = squeak_db.get_squeak_entries_for_address(
        address=address_str,
        limit=200,
        last_entry=None,
    )

    assert len(address_squeak_entries) == len(inserted_squeak_hashes)


def test_get_address_squeak_entries_other_address(
        squeak_db,
        inserted_squeak_hashes,
):
    # Get the address squeak entries for a different address.
    other_address_str = str(gen_address())
    address_squeak_entries = squeak_db.get_squeak_entries_for_address(
        address=other_address_str,
        limit=200,
        last_entry=None,
    )

    assert len(address_squeak_entries) == 0


def test_get_search_squeak_entries(
        squeak_db,
        unlocked_squeak_hash,
):
    # Get the search squeak entries.
    squeak_entries = squeak_db.get_squeak_entries_for_text_search(
        search_text="hello",
        limit=200,
        last_entry=None,
    )

    assert len(squeak_entries) == 1


def test_get_search_squeak_entries_other_text(
        squeak_db,
        unlocked_squeak_hash,
):
    # Get the search squeak entries.
    squeak_entries = squeak_db.get_squeak_entries_for_text_search(
        search_text="goodbye",
        limit=200,
        last_entry=None,
    )

    assert len(squeak_entries) == 0


def test_get_ancestor_squeak_entries(
        squeak_db,
        inserted_squeak_hash,
        inserted_reply_squeak_hash,
):
    # Get the ancestor squeak entries.
    squeak_entries = squeak_db.get_thread_ancestor_squeak_entries(
        squeak_hash=inserted_reply_squeak_hash,
    )

    assert len(squeak_entries) == 2


def test_get_ancestor_squeak_entries_no_ancestors(
        squeak_db,
        inserted_squeak_hash,
):
    # Get the ancestor squeak entries.
    squeak_entries = squeak_db.get_thread_ancestor_squeak_entries(
        squeak_hash=inserted_squeak_hash,
    )

    assert len(squeak_entries) == 1


def test_get_ancestor_squeak_entries_no_ancestors_or_root(
        squeak_db,
):
    # Get the ancestor squeak entries.
    squeak_entries = squeak_db.get_thread_ancestor_squeak_entries(
        squeak_hash=gen_random_hash(),
    )

    assert len(squeak_entries) == 0


def test_get_reply_squeak_entries(
        squeak_db,
        inserted_squeak_hash,
        inserted_reply_squeak_hash,
):
    # Get the reply squeak entries.
    squeak_entries = squeak_db.get_thread_reply_squeak_entries(
        squeak_hash=inserted_squeak_hash,
        limit=200,
        last_entry=None,
    )

    assert len(squeak_entries) == 1


def test_get_reply_squeak_entries_no_replies(
        squeak_db,
        inserted_squeak_hash,
):
    # Get the reply squeak entries.
    squeak_entries = squeak_db.get_thread_reply_squeak_entries(
        squeak_hash=inserted_squeak_hash,
        limit=200,
        last_entry=None,
    )

    assert len(squeak_entries) == 0


def test_lookup_squeaks_all(
        squeak_db,
        inserted_squeak_hashes,
):
    squeak_hashes = squeak_db.lookup_squeaks(
        addresses=None,
        min_block=None,
        max_block=None,
        reply_to_hash=None,
        include_locked=True,
    )

    assert len(squeak_hashes) == len(inserted_squeak_hashes)


def test_lookup_squeaks_use_address(
        squeak_db,
        inserted_squeak_hashes,
        address_str,
):
    other_address_str = str(gen_address())
    squeak_hashes = squeak_db.lookup_squeaks(
        addresses=[address_str, other_address_str],
        min_block=None,
        max_block=None,
        reply_to_hash=None,
        include_locked=True,
    )

    assert len(squeak_hashes) == len(inserted_squeak_hashes)


def test_lookup_squeaks_use_address_no_matches(
        squeak_db,
        inserted_squeak_hashes,
        address_str,
):
    other_address_str = str(gen_address())
    squeak_hashes = squeak_db.lookup_squeaks(
        addresses=[other_address_str],
        min_block=None,
        max_block=None,
        reply_to_hash=None,
        include_locked=True,
    )

    assert len(squeak_hashes) == 0


def test_lookup_squeaks_min_block(
        squeak_db,
        inserted_squeak_hashes,
):
    min_block = 35
    squeak_hashes = squeak_db.lookup_squeaks(
        addresses=None,
        min_block=min_block,
        max_block=None,
        reply_to_hash=None,
        include_locked=True,
    )

    assert len(squeak_hashes) == len(inserted_squeak_hashes) - min_block


def test_lookup_squeaks_max_block(
        squeak_db,
        inserted_squeak_hashes,
):
    max_block = 27
    squeak_hashes = squeak_db.lookup_squeaks(
        addresses=None,
        min_block=None,
        max_block=max_block,
        reply_to_hash=None,
        include_locked=True,
    )

    assert len(squeak_hashes) == max_block + 1


def test_lookup_squeaks_reply_to(
        squeak_db,
        inserted_squeak_hash,
        inserted_reply_squeak_hash,
):
    squeak_hashes = squeak_db.lookup_squeaks(
        addresses=None,
        min_block=None,
        max_block=None,
        reply_to_hash=inserted_squeak_hash,
        include_locked=True,
    )

    assert len(squeak_hashes) == 1


def test_lookup_squeaks_reply_to_none(
        squeak_db,
        inserted_squeak_hash,
):
    squeak_hashes = squeak_db.lookup_squeaks(
        addresses=None,
        min_block=None,
        max_block=None,
        reply_to_hash=inserted_squeak_hash,
        include_locked=True,
    )

    assert len(squeak_hashes) == 0


def test_lookup_squeaks_unlocked_all(
        squeak_db,
        unlocked_squeak_hash,
):
    squeak_hashes = squeak_db.lookup_squeaks(
        addresses=None,
        min_block=None,
        max_block=None,
        reply_to_hash=None,
        include_locked=False,
    )

    assert len(squeak_hashes) == 1


def test_lookup_squeaks_unlocked_all_none(
        squeak_db,
        inserted_squeak_hash,
):
    squeak_hashes = squeak_db.lookup_squeaks(
        addresses=None,
        min_block=None,
        max_block=None,
        reply_to_hash=None,
        include_locked=False,
    )

    assert len(squeak_hashes) == 0


def test_get_number_of_squeaks(
        squeak_db,
        inserted_squeak_hashes,
):
    num_squeaks = squeak_db.get_number_of_squeaks()

    assert num_squeaks == len(inserted_squeak_hashes)


def test_number_of_squeaks_with_address_in_block_range(
        squeak_db,
        address_str,
        inserted_squeak_hashes,
):
    min_block = 43
    max_block = 91
    num_squeaks = squeak_db.number_of_squeaks_with_address_in_block_range(
        address=address_str,
        min_block=min_block,
        max_block=max_block,
    )

    assert num_squeaks == max_block - min_block + 1


def test_get_old_squeaks_to_delete(
        squeak_db,
        followed_squeak_hashes,
):
    current_time_ms = int(time.time() * 1000)
    time_elapsed_s = 56789
    fake_current_time_ms = current_time_ms + 1000 * time_elapsed_s

    # TODO: set up test so it returns positive number of squeaks to delete.
    with mock.patch.object(SqueakDb, 'timestamp_now_ms', new_callable=mock.PropertyMock) as mock_timestamp_ms:
        mock_timestamp_ms.return_value = fake_current_time_ms

        interval_s = time_elapsed_s - 10
        hashes_to_delete = squeak_db.get_old_squeaks_to_delete(
            interval_s=interval_s,
        )

        assert len(hashes_to_delete) == 100


def test_get_old_squeaks_to_delete_none(
        squeak_db,
        followed_squeak_hashes,
):
    current_time_ms = int(time.time() * 1000)
    time_elapsed_s = 56789
    fake_current_time_ms = current_time_ms + 1000 * time_elapsed_s

    with mock.patch.object(SqueakDb, 'timestamp_now_ms', new_callable=mock.PropertyMock) as mock_timestamp_ms:
        mock_timestamp_ms.return_value = fake_current_time_ms

        interval_s = time_elapsed_s + 10
        hashes_to_delete = squeak_db.get_old_squeaks_to_delete(
            interval_s=interval_s,
        )

        assert len(hashes_to_delete) == 0


def test_get_old_squeaks_to_delete_none_signing_profile(
        squeak_db,
        authored_squeak_hashes,
):
    """
    `get_old_squeaks_to_delete` Method should return 0 results because
    all squeaks are authored by the signing profile.

    """
    current_time_ms = int(time.time() * 1000)
    time_elapsed_s = 56789
    fake_current_time_ms = current_time_ms + 1000 * time_elapsed_s

    with mock.patch.object(SqueakDb, 'timestamp_now_ms', new_callable=mock.PropertyMock) as mock_timestamp_ms:
        mock_timestamp_ms.return_value = fake_current_time_ms

        interval_s = time_elapsed_s - 10
        hashes_to_delete = squeak_db.get_old_squeaks_to_delete(
            interval_s=interval_s,
        )

        assert len(hashes_to_delete) == 0


def test_get_old_squeaks_to_delete_none_liked(
        squeak_db,
        liked_squeak_hashes,
):
    """
    `get_old_squeaks_to_delete` Method should return 0 results because
    all squeaks are liked.

    """
    current_time_ms = int(time.time() * 1000)
    time_elapsed_s = 56789
    fake_current_time_ms = current_time_ms + 1000 * time_elapsed_s

    with mock.patch.object(SqueakDb, 'timestamp_now_ms', new_callable=mock.PropertyMock) as mock_timestamp_ms:
        mock_timestamp_ms.return_value = fake_current_time_ms

        interval_s = time_elapsed_s - 10
        hashes_to_delete = squeak_db.get_old_squeaks_to_delete(
            interval_s=interval_s,
        )

        assert len(hashes_to_delete) == 0


def test_get_profiles(
        squeak_db,
        inserted_contact_profile_ids,
        inserted_signing_profile_ids,
):
    profiles = squeak_db.get_profiles()

    assert len(profiles) == len(inserted_contact_profile_ids) + \
        len(inserted_signing_profile_ids)


def test_get_signing_profiles(
        squeak_db,
        inserted_signing_profile_ids,
):
    profiles = squeak_db.get_signing_profiles()

    assert len(profiles) == len(inserted_signing_profile_ids)


def test_get_signing_profiles_none(
        squeak_db,
        inserted_contact_profile_ids,
):
    profiles = squeak_db.get_signing_profiles()

    assert len(profiles) == 0


def test_get_contact_profiles(
        squeak_db,
        inserted_contact_profile_ids,
):
    profiles = squeak_db.get_contact_profiles()

    assert len(profiles) == len(inserted_contact_profile_ids)


def test_get_contact_profiles_none(
        squeak_db,
        inserted_signing_profile_ids,
):
    profiles = squeak_db.get_contact_profiles()

    assert len(profiles) == 0


def test_get_following_profiles(
        squeak_db,
        followed_contact_profile_ids,
):
    profiles = squeak_db.get_following_profiles()

    assert len(profiles) == len(followed_contact_profile_ids)


def test_get_profile(
        squeak_db,
        inserted_signing_profile_id,
        signing_profile,
):
    profile = squeak_db.get_profile(inserted_signing_profile_id)

    assert profile == signing_profile._replace(
        profile_id=inserted_signing_profile_id)


def test_get_profile_by_address(
        squeak_db,
        inserted_signing_profile_id,
        signing_profile,
        address_str,
):
    profile = squeak_db.get_profile_by_address(address_str)

    assert profile == signing_profile._replace(
        profile_id=inserted_signing_profile_id)


def test_get_profile_by_address_none(
        squeak_db,
        inserted_signing_profile_id,
        signing_profile,
):
    random_address = str(gen_address())
    profile = squeak_db.get_profile_by_address(random_address)

    assert profile is None


def test_get_profile_by_name(
        squeak_db,
        inserted_signing_profile_id,
        signing_profile,
        signing_profile_name,
):
    profile = squeak_db.get_profile_by_name(signing_profile_name)

    assert profile == signing_profile._replace(
        profile_id=inserted_signing_profile_id)


def test_get_profile_by_name_none(
        squeak_db,
        inserted_signing_profile_id,
        signing_profile,
):
    other_name = "fake_name_9876"
    profile = squeak_db.get_profile_by_name(other_name)

    assert profile is None


def test_get_squeak_peers(
        squeak_db,
        inserted_squeak_peer_ids,
):
    peers = squeak_db.get_peers()

    assert len(peers) == len(inserted_squeak_peer_ids)


def test_get_autoconnect_squeak_peers(
        squeak_db,
        autoconnect_squeak_peer_ids,
):
    peers = squeak_db.get_autoconnect_peers()

    assert len(peers) == len(autoconnect_squeak_peer_ids)


def test_get_autoconnect_squeak_peers_none(
        squeak_db,
        inserted_squeak_peer_ids,
):
    peers = squeak_db.get_autoconnect_peers()

    assert len(peers) == 0


def test_set_peer_name(squeak_db, peer_with_new_name_id, new_peer_name):
    peer = squeak_db.get_peer(peer_with_new_name_id)

    assert peer.peer_name == new_peer_name


def test_get_deleted_peer(squeak_db, deleted_peer_id):
    retrieved_peer = squeak_db.get_peer(deleted_peer_id)

    assert retrieved_peer is None


def test_get_received_offer(squeak_db, inserted_received_offer_id, received_offer):
    retrieved_received_offer = squeak_db.get_received_offer(
        inserted_received_offer_id)

    assert retrieved_received_offer._replace(
        received_offer_id=None,
    ) == received_offer


def test_duplicate_inserted_received_offer(squeak_db, duplicate_inserted_received_offer_id):
    assert duplicate_inserted_received_offer_id is None


def test_get_received_offer_none(squeak_db, inserted_received_offer_id, received_offer):
    retrieved_received_offer = squeak_db.get_received_offer(
        -1,
    )

    assert retrieved_received_offer is None


def test_get_received_offers(squeak_db, inserted_received_offer_id, squeak_hash, creation_date, expiry):
    expire_time_s = creation_date + expiry
    current_time_s = expire_time_s - 10
    fake_current_time_ms = current_time_s * 1000

    with mock.patch.object(SqueakDb, 'timestamp_now_ms', new_callable=mock.PropertyMock) as mock_timestamp_ms:
        mock_timestamp_ms.return_value = fake_current_time_ms

        received_offers = squeak_db.get_received_offers(
            squeak_hash=squeak_hash,
        )

        assert len(received_offers) == 1


def test_get_received_offers_expired_none(squeak_db, inserted_received_offer_id, squeak_hash, creation_date, expiry):
    expire_time_s = creation_date + expiry
    current_time_s = expire_time_s + 10
    fake_current_time_ms = current_time_s * 1000

    with mock.patch.object(SqueakDb, 'timestamp_now_ms', new_callable=mock.PropertyMock) as mock_timestamp_ms:
        mock_timestamp_ms.return_value = fake_current_time_ms

        received_offers = squeak_db.get_received_offers(
            squeak_hash=squeak_hash,
        )

        assert len(received_offers) == 0


def test_get_received_offers_other_squeak_hash(squeak_db, inserted_received_offer_id):
    received_offers = squeak_db.get_received_offers(
        squeak_hash=gen_random_hash(),
    )

    assert len(received_offers) == 0
