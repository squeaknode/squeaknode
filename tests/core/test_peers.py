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

from squeaknode.core.peer_address import PeerAddress
from squeaknode.core.peers import create_saved_peer


@pytest.fixture
def peer_name():
    yield "fake_peer_name"


@pytest.fixture
def peer_address():
    yield PeerAddress(
        host="fake_host",
        port=8765,
    )


@pytest.fixture
def peer_address_with_no_port():
    yield PeerAddress(
        host="fake_host",
        port=0,
    )


@pytest.fixture
def default_peer_port():
    yield 55555


def test_create_saved_peer(peer_name, peer_address, default_peer_port):
    peer = create_saved_peer(
        peer_name,
        peer_address,
        default_peer_port,
    )

    assert peer.peer_name == peer_name
    assert peer.address == PeerAddress(
        host=peer_address.host,
        port=peer_address.port,
    )


def test_create_saved_peer_empty_name(peer_address, default_peer_port):
    with pytest.raises(Exception) as excinfo:
        create_saved_peer("", peer_address, default_peer_port)
    assert "Peer name cannot be empty." in str(excinfo.value)


def test_create_saved_peer_default_port(peer_name, peer_address_with_no_port, default_peer_port):
    peer = create_saved_peer(
        peer_name,
        peer_address_with_no_port,
        default_peer_port,
    )

    assert peer.peer_name == peer_name
    assert peer.address == PeerAddress(
        host=peer_address_with_no_port.host,
        port=default_peer_port,
    )
