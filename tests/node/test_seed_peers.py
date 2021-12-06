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

from squeaknode.core.peer_address import Network
from squeaknode.core.peer_address import PeerAddress
from squeaknode.core.seed_peer import SeedPeer
from squeaknode.core.seed_peer import SeedPeerConfig
from squeaknode.db.squeak_db import SqueakDb
from squeaknode.node.seed_peers import SeedPeers


@pytest.fixture
def db_engine():
    yield create_engine('sqlite://')


@pytest.fixture
def squeak_db(db_engine):
    db = SqueakDb(db_engine)
    db.init()
    yield db


# @pytest.fixture()
# def network():
#     yield "mainnet"


@pytest.fixture()
def seed_peer_name():
    yield 'test_seed_peer'


@pytest.fixture()
def seed_peer_address():
    yield PeerAddress(
        network=Network.IPV4,
        host='test_seed_peer.com',
        port=18555,
    )


@pytest.fixture()
def seed_peer_dict(seed_peer_name, seed_peer_address):
    yield {
        seed_peer_name: seed_peer_address
    }


@pytest.fixture()
def seed_peers(squeak_db, seed_peer_dict):
    yield SeedPeers(squeak_db, seed_peer_dict)


@pytest.fixture()
def seed_peer_config(seed_peer_name):
    yield SeedPeerConfig(
        peer_name=seed_peer_name,
        autoconnect=True,
        share_for_free=False,
    )


def test_get_seed_peers(seed_peers, seed_peer_name, seed_peer_address, seed_peer_config):
    with mock.patch.object(seed_peers, 'get_config_from_db', autospec=True, return_value=None):
        peers = seed_peers.get_seed_peers()

    assert peers == [
        SeedPeer(
            peer_name=seed_peer_name,
            address=seed_peer_address,
            config=seed_peer_config,
        )
    ]


def test_get_seed_peer(seed_peers, seed_peer_name, seed_peer_address, seed_peer_config):
    with mock.patch.object(seed_peers, 'get_config_from_db', autospec=True, return_value=None):
        peer = seed_peers.get_seed_peer(seed_peer_name)

    assert peer == SeedPeer(
        peer_name=seed_peer_name,
        address=seed_peer_address,
        config=seed_peer_config,
    )


def test_get_seed_peer_none(seed_peers):
    with mock.patch.object(seed_peers, 'get_config_from_db', autospec=True, return_value=None):
        peer = seed_peers.get_seed_peer('fake_seed_peer_name')

    assert peer is None


def test_set_autoconnect(seed_peers, seed_peer_name):
    peer = seed_peers.get_seed_peer(seed_peer_name)

    assert peer.config.autoconnect is True

    peer = seed_peers.set_seed_peer_autoconnect(seed_peer_name, False)
    peer = seed_peers.get_seed_peer(seed_peer_name)

    assert peer.config.autoconnect is False

    peer = seed_peers.set_seed_peer_autoconnect(seed_peer_name, True)
    peer = seed_peers.get_seed_peer(seed_peer_name)

    assert peer.config.autoconnect is True


def test_set_share_for_free(seed_peers, seed_peer_name):
    peer = seed_peers.get_seed_peer(seed_peer_name)

    assert peer.config.share_for_free is False

    peer = seed_peers.set_seed_peer_share_for_free(seed_peer_name, False)
    peer = seed_peers.get_seed_peer(seed_peer_name)

    assert peer.config.share_for_free is False

    peer = seed_peers.set_seed_peer_share_for_free(seed_peer_name, True)
    peer = seed_peers.get_seed_peer(seed_peer_name)

    assert peer.config.share_for_free is True
