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

from squeaknode.core.peers import create_saved_peer
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


@pytest.fixture
def inserted_squeak_hash(squeak_db, squeak, block_header):
    yield squeak_db.insert_squeak(squeak, block_header)


@pytest.fixture
def unlocked_squeak_hash(squeak_db, squeak, inserted_squeak_hash, secret_key, squeak_content):
    squeak_db.set_squeak_decryption_key(
        inserted_squeak_hash, secret_key, squeak_content)
    yield inserted_squeak_hash


@pytest.fixture
def inserted_signing_profile_id(squeak_db, signing_profile):
    yield squeak_db.insert_profile(signing_profile)


@pytest.fixture
def inserted_signing_profile(squeak_db, inserted_signing_profile_id):
    yield squeak_db.get_profile(inserted_signing_profile_id)


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
def followed_contact_profile(squeak_db, followed_contact_profile_id):
    yield squeak_db.get_profile(
        followed_contact_profile_id,
    )


@pytest.fixture
def unfollowed_contact_profile_id(squeak_db, followed_contact_profile_id):
    squeak_db.set_profile_following(
        followed_contact_profile_id,
        False,
    )
    yield followed_contact_profile_id


@pytest.fixture
def unfollowed_contact_profile(squeak_db, unfollowed_contact_profile_id):
    yield squeak_db.get_profile(
        unfollowed_contact_profile_id,
    )


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
        followed_contact_profile,
):
    yield inserted_squeak_hashes


@pytest.fixture
def unfollowed_squeak_hashes(
        squeak_db,
        inserted_squeak_hashes,
        unfollowed_contact_profile,
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
def peer(peer_address):
    yield create_saved_peer(
        "fake_peer_name",
        peer_address,
    )


@pytest.fixture
def inserted_peer_id(squeak_db, peer):
    yield squeak_db.insert_peer(peer)
