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

from squeaknode.db.squeak_db import SqueakDb
from squeaknode.node.saved_peers import SavedPeers


@pytest.fixture
def db_engine():
    yield create_engine('sqlite://')


@pytest.fixture
def squeak_db(db_engine):
    db = SqueakDb(db_engine)
    db.init()
    yield db


@pytest.fixture()
def saved_peers(squeak_db):
    # TODO: Use a mock db.
    yield SavedPeers(squeak_db)


@pytest.fixture()
def saved_peer_name():
    yield "fake_peer_name"


@pytest.fixture()
def inserted_saved_peer(saved_peers, saved_peer_name, peer_address):
    yield saved_peers.create_saved_peer(
        saved_peer_name,
        peer_address,
    )


def test_get_saved_peers(saved_peers, inserted_saved_peer, saved_peer_name):
    peers = saved_peers.get_saved_peers()

    assert len(peers) == 1
    assert peers[0].peer_name == saved_peer_name


def test_get_saved_peer(saved_peers, inserted_saved_peer, saved_peer_name):
    peer = saved_peers.get_saved_peer(inserted_saved_peer)

    assert peer is not None
    assert peer.peer_name == saved_peer_name


def test_get_saved_peer_by_address(saved_peers, inserted_saved_peer, peer_address, saved_peer_name):
    peer = saved_peers.get_saved_peer_by_address(peer_address)

    assert peer is not None
    assert peer.peer_name == saved_peer_name


def test_rename_saved_peer(saved_peers, inserted_saved_peer):
    peer = saved_peers.rename_peer(inserted_saved_peer, 'new_peer_name')
    peer = saved_peers.get_saved_peer(inserted_saved_peer)

    assert peer.peer_name == 'new_peer_name'


def test_delete_saved_peer(saved_peers, inserted_saved_peer):
    peer = saved_peers.delete_peer(inserted_saved_peer)
    peer = saved_peers.get_saved_peer(inserted_saved_peer)

    assert peer is None


def test_set_autoconnect(saved_peers, inserted_saved_peer):
    peer = saved_peers.get_saved_peer(inserted_saved_peer)

    assert peer.autoconnect is False

    peer = saved_peers.set_peer_autoconnect(inserted_saved_peer, False)
    peer = saved_peers.get_saved_peer(inserted_saved_peer)

    assert peer.autoconnect is False

    peer = saved_peers.set_peer_autoconnect(inserted_saved_peer, True)
    peer = saved_peers.get_saved_peer(inserted_saved_peer)

    assert peer.autoconnect is True


def test_set_share_for_free(saved_peers, inserted_saved_peer):
    peer = saved_peers.get_saved_peer(inserted_saved_peer)

    assert peer.share_for_free is False

    peer = saved_peers.set_peer_share_for_free(
        inserted_saved_peer, False)
    peer = saved_peers.get_saved_peer(inserted_saved_peer)

    assert peer.share_for_free is False

    peer = saved_peers.set_peer_share_for_free(
        inserted_saved_peer, True)
    peer = saved_peers.get_saved_peer(inserted_saved_peer)

    assert peer.share_for_free is True


def test_get_autoconnect_peers(saved_peers):
    peers = saved_peers.get_autoconnect_addresses()

    assert peers == []
