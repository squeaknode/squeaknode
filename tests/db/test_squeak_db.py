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
