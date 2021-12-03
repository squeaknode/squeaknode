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

from squeaknode.core.seed_peer import SeedPeer
from squeaknode.node.seed_peers import SEED_PEERS
from squeaknode.node.seed_peers import SeedPeers


@pytest.fixture()
def seed_peers():
    # TODO: Use a mock db.
    yield SeedPeers(None)


def test_get_seed_peers(seed_peers):
    peers = seed_peers.get_seed_peers()

    assert peers == [
        SeedPeer(
            peer_name='squeakhub',
            address=SEED_PEERS['squeakhub'],
            autoconnect=True,
            share_for_free=False,
        )
    ]


def test_get_seed_peer(seed_peers):
    peer = seed_peers.get_seed_peer('squeakhub')

    assert peer == SeedPeer(
        peer_name='squeakhub',
        address=SEED_PEERS['squeakhub'],
        autoconnect=True,
        share_for_free=False,
    )


def test_get_seed_peer_none(seed_peers):
    peer = seed_peers.get_seed_peer('fake_seed_peer_name')

    assert peer is None
