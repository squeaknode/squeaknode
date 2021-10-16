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
from squeaknode.core.squeaks import get_hash


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


def test_get_squeak_entry(squeak_db, squeak, block_header, address_str, inserted_squeak_hash):
    retrieved_squeak_entry = squeak_db.get_squeak_entry(inserted_squeak_hash)

    assert retrieved_squeak_entry.squeak_hash == inserted_squeak_hash
    assert retrieved_squeak_entry.address == address_str
    assert retrieved_squeak_entry.content is None
    assert retrieved_squeak_entry.block_time == block_header.nTime


def test_get_missing_squeak_entry(squeak_db, squeak):
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


def test_set_squeak_liked(squeak_db, liked_squeak_hash):
    retrieved_squeak_entry = squeak_db.get_squeak_entry(liked_squeak_hash)

    assert retrieved_squeak_entry.liked_time_ms is not None


def test_set_squeak_unliked(squeak_db, unliked_squeak_hash):
    retrieved_squeak_entry = squeak_db.get_squeak_entry(unliked_squeak_hash)

    assert retrieved_squeak_entry.liked_time_ms is None


def test_get_peer(squeak_db, peer, inserted_peer_id):
    retrieved_peer = squeak_db.get_peer(inserted_peer_id)

    assert retrieved_peer.peer_name == peer.peer_name
    assert retrieved_peer.address == peer.address
