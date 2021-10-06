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


def test_insert_get_squeak(squeak_db, squeak, block_header):
    squeak_hash = squeak_db.insert_squeak(squeak, block_header)
    retrieved_squeak = squeak_db.get_squeak(squeak_hash)

    assert retrieved_squeak == squeak


def test_insert_duplicate_squeak(squeak_db, squeak, block_header):
    first_squeak_hash = squeak_db.insert_squeak(squeak, block_header)
    second_squeak_hash = squeak_db.insert_squeak(squeak, block_header)

    assert first_squeak_hash is not None
    assert second_squeak_hash is None


def test_get_missing_squeak(squeak_db, squeak):
    squeak_hash = get_hash(squeak)
    retrieved_squeak = squeak_db.get_squeak(squeak_hash)

    assert retrieved_squeak is None


def test_get_squeak_entry(squeak_db, squeak, block_header, address):
    squeak_hash = squeak_db.insert_squeak(squeak, block_header)
    retrieved_squeak_entry = squeak_db.get_squeak_entry(squeak_hash)

    assert retrieved_squeak_entry.squeak_hash == squeak_hash
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
        block_header,
        secret_key,
        address,
        squeak_content,
):
    squeak_hash = squeak_db.insert_squeak(squeak, block_header)
    squeak_db.set_squeak_decryption_key(
        squeak_hash, secret_key, squeak_content)
    retrieved_squeak_entry = squeak_db.get_squeak_entry(squeak_hash)
    retrieved_secret_key = squeak_db.get_squeak_secret_key(squeak_hash)

    assert retrieved_squeak_entry.squeak_hash == squeak_hash
    assert retrieved_squeak_entry.content == squeak_content
    assert retrieved_secret_key == secret_key


def test_get_missing_squeak_secret_key(
        squeak_db,
        squeak,
        block_header,
):
    squeak_hash = squeak_db.insert_squeak(squeak, block_header)
    retrieved_secret_key = squeak_db.get_squeak_secret_key(squeak_hash)

    assert retrieved_secret_key is None


def test_get_timeline_squeak_entries(
        squeak_db,
        signing_key,
        signing_profile,
        contact_profile,
):
    squeak_1, header_1 = gen_squeak_with_block_header(signing_key, 5001)
    squeak_2, header_2 = gen_squeak_with_block_header(signing_key, 5002)
    squeak_3, header_3 = gen_squeak_with_block_header(signing_key, 5003)
    squeak_4, header_4 = gen_squeak_with_block_header(signing_key, 5004)
    squeak_5, header_5 = gen_squeak_with_block_header(signing_key, 5005)

    squeak_hash_1 = squeak_db.insert_squeak(squeak_1, header_1)
    squeak_hash_2 = squeak_db.insert_squeak(squeak_2, header_2)
    squeak_hash_3 = squeak_db.insert_squeak(squeak_3, header_3)
    squeak_hash_4 = squeak_db.insert_squeak(squeak_4, header_4)
    squeak_hash_5 = squeak_db.insert_squeak(squeak_5, header_5)

    assert squeak_hash_1 is not None
    assert squeak_hash_2 is not None
    assert squeak_hash_3 is not None
    assert squeak_hash_4 is not None
    assert squeak_hash_5 is not None

    # Insert the contact profile and ensure that it is followed.
    profile_id = squeak_db.insert_profile(contact_profile)
    squeak_db.set_profile_following(profile_id, True)

    # TODO: get_timeline_squeak_entries only returns followed squeaks.
    timeline_squeak_entries = squeak_db.get_timeline_squeak_entries(
        limit=2,
        last_entry=None,
    )

    assert len(timeline_squeak_entries) == 2


def test_get_signing_profile(squeak_db, signing_key, signing_profile):
    profile_id = squeak_db.insert_profile(signing_profile)
    retrieved_profile = squeak_db.get_profile(profile_id)

    assert retrieved_profile.profile_name == signing_profile.profile_name
    assert retrieved_profile.private_key == signing_profile.private_key


def test_get_contact_profile(squeak_db, address, contact_profile):
    profile_id = squeak_db.insert_profile(contact_profile)
    retrieved_profile = squeak_db.get_profile(profile_id)

    assert retrieved_profile.profile_name == contact_profile.profile_name
    assert retrieved_profile.address == contact_profile.address
