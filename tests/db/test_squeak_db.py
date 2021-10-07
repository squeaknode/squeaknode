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
from sqlalchemy import create_engine

from squeaknode.core.squeaks import get_hash
from squeaknode.db.squeak_db import SqueakDb
from tests.utils import gen_contact_profile
from tests.utils import gen_signing_profile
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
def squeak_with_block_header(signing_key):
    yield gen_squeak_with_block_header(
        signing_key=signing_key,
        block_height=7777,
    )


@pytest.fixture
def squeak(squeak_with_block_header):
    squeak, _ = squeak_with_block_header
    yield squeak


@pytest.fixture
def block_header(squeak_with_block_header):
    _, block_header = squeak_with_block_header
    yield block_header


@pytest.fixture
def signing_profile_name():
    yield "fake_signing_profile_name"


@pytest.fixture
def contact_profile_name():
    yield "fake_contact_profile_name"


@pytest.fixture
def signing_profile(signing_profile_name, signing_key):
    yield gen_signing_profile(
        signing_profile_name,
        str(signing_key),
    )


@pytest.fixture
def contact_profile(contact_profile_name, address):
    yield gen_contact_profile(
        contact_profile_name,
        str(address),
    )


@pytest.fixture
def inserted_squeak_hash(squeak_db, squeak, block_header):
    yield squeak_db.insert_squeak(squeak, block_header)


@pytest.fixture
def unlocked_squeak_hash(squeak_db, squeak, inserted_squeak_hash, secret_key, squeak_content):
    squeak_db.set_squeak_decryption_key(
        inserted_squeak_hash, secret_key, squeak_content)
    yield inserted_squeak_hash


@pytest.fixture
def inserted_signing_profile(squeak_db, signing_profile):
    profile_id = squeak_db.insert_profile(signing_profile)
    yield squeak_db.get_profile(profile_id)


@pytest.fixture
def inserted_contact_profile(squeak_db, contact_profile):
    profile_id = squeak_db.insert_profile(contact_profile)
    yield squeak_db.get_profile(profile_id)


@pytest.fixture
def followed_contact_profile(squeak_db, inserted_contact_profile):
    squeak_db.set_profile_following(
        inserted_contact_profile.profile_id,
        True,
    )
    yield squeak_db.get_profile(
        inserted_contact_profile.profile_id,
    )


@pytest.fixture
def unfollowed_contact_profile(squeak_db, followed_contact_profile):
    squeak_db.set_profile_following(
        followed_contact_profile.profile_id,
        False,
    )
    yield squeak_db.get_profile(
        followed_contact_profile.profile_id,
    )


@pytest.fixture
def followed_squeak_hashes(
        squeak_db,
        signing_key,
        followed_contact_profile,
):
    ret = []
    for i in range(100):
        squeak, header = gen_squeak_with_block_header(signing_key, i)
        squeak_hash = squeak_db.insert_squeak(squeak, header)
        ret.append(squeak_hash)
    yield ret


@pytest.fixture
def unfollowed_squeak_hashes(
        squeak_db,
        signing_key,
        unfollowed_contact_profile,
):
    ret = []
    for i in range(100):
        squeak, header = gen_squeak_with_block_header(signing_key, i)
        squeak_hash = squeak_db.insert_squeak(squeak, header)
        ret.append(squeak_hash)
    yield ret


@pytest.fixture
def liked_squeak_hashes(
        squeak_db,
        signing_key,
):
    ret = []
    for i in range(100):
        squeak, header = gen_squeak_with_block_header(signing_key, i)
        squeak_hash = squeak_db.insert_squeak(squeak, header)
        squeak_db.set_squeak_liked(squeak_hash)
        ret.append(squeak_hash)
    yield ret


@pytest.fixture
def unliked_squeak_hashes(
        squeak_db,
        liked_squeak_hashes,
):
    for squeak_hash in liked_squeak_hashes:
        squeak_db.set_squeak_unliked(squeak_hash)
    yield liked_squeak_hashes


def test_get_squeak(squeak_db, squeak, inserted_squeak_hash):
    retrieved_squeak = squeak_db.get_squeak(inserted_squeak_hash)

    assert retrieved_squeak == squeak


def test_insert_duplicate_squeak(squeak_db, squeak, block_header, inserted_squeak_hash):
    insert_result = squeak_db.insert_squeak(squeak, block_header)

    assert insert_result is None


def test_get_missing_squeak(squeak_db, squeak):
    squeak_hash = get_hash(squeak)
    retrieved_squeak = squeak_db.get_squeak(squeak_hash)

    assert retrieved_squeak is None


def test_get_squeak_entry(squeak_db, squeak, block_header, address, inserted_squeak_hash):
    retrieved_squeak_entry = squeak_db.get_squeak_entry(inserted_squeak_hash)

    assert retrieved_squeak_entry.squeak_hash == inserted_squeak_hash
    assert retrieved_squeak_entry.address == address
    assert retrieved_squeak_entry.content is None
    assert retrieved_squeak_entry.block_time == block_header.nTime


def test_get_missing_squeak_entry(squeak_db, squeak, address):
    squeak_hash = get_hash(squeak)
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


def test_get_secret_key_missing_squeak(squeak_db, squeak):
    squeak_hash = get_hash(squeak)
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


def test_get_signing_profile(squeak_db, signing_profile, inserted_signing_profile):

    assert inserted_signing_profile.profile_id is not None
    assert inserted_signing_profile.profile_name == signing_profile.profile_name
    assert inserted_signing_profile.private_key == signing_profile.private_key
    assert inserted_signing_profile.address == signing_profile.address


def test_get_contact_profile(squeak_db, contact_profile, inserted_contact_profile):

    assert inserted_contact_profile.profile_id is not None
    assert inserted_contact_profile.private_key is None
    assert inserted_contact_profile.profile_name == contact_profile.profile_name
    assert inserted_contact_profile.address == contact_profile.address


def test_set_profile_following(squeak_db, followed_contact_profile):

    assert followed_contact_profile.following


def test_set_profile_unfollowing(squeak_db, unfollowed_contact_profile):

    assert not unfollowed_contact_profile.following


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


def test_set_squeak_liked(squeak_db, signing_key):
    squeak, header = gen_squeak_with_block_header(signing_key, 5001)
    squeak_hash = squeak_db.insert_squeak(squeak, header)
    squeak_db.set_squeak_liked(squeak_hash)
    retrieved_squeak_entry = squeak_db.get_squeak_entry(squeak_hash)

    assert retrieved_squeak_entry.liked_time_ms is not None

    squeak_db.set_squeak_unliked(squeak_hash)
    retrieved_squeak_entry = squeak_db.get_squeak_entry(squeak_hash)

    assert retrieved_squeak_entry.liked_time_ms is None
