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
import queue
import socket
import threading
from concurrent.futures import ThreadPoolExecutor
from contextlib import closing

import mock
import pytest

from squeaknode.core.peer_address import PeerAddress
from squeaknode.network.connection_manager import ConnectionManager
from squeaknode.node.squeak_controller import SqueakController


TEST_SOCKET_PORT = 19999
SOCKET_CONNECT_TIMEOUT = 10


def accept_connections(listen_socket, started_event):
    try:
        print('Trying to bind and listen on port: {}'.format(
            TEST_SOCKET_PORT), flush=True)
        listen_socket.bind(('', TEST_SOCKET_PORT))
        listen_socket.listen()
        started_event.set()
        print('Started event set.', flush=True)
        peer_socket, address = listen_socket.accept()
        # host, port = address
        # peer_address = PeerAddress(
        #     host=host,
        #     port=port,
        # )
        peer_socket.setblocking(True)
        return peer_socket
    except Exception as e:
        print(e)
        started_event.set()
        return e


def make_connection(peer_socket, started):
    address = ('localhost', TEST_SOCKET_PORT)
    started.wait()
    print('Conecting to address: {}'.format(address))
    try:
        peer_socket.settimeout(SOCKET_CONNECT_TIMEOUT)
        peer_socket.connect(address)
        peer_socket.setblocking(True)
        return peer_socket
    except Exception:
        print('Failed to connect to {}'.format(address))


def start_connection(
        connection_manager,
        connected_event,
        disconnect_event,
        disconnected_event,
        socket,
        remote_address,
        is_outbound,
        squeak_controller,
        result_q,
):
    if is_outbound:
        print('------Starting outbound connection------')
    else:
        print('------Starting inbound connection------')
    with connection_manager.connect(
            socket,
            remote_address,
            is_outbound,
            squeak_controller,
            result_q,
    ):
        connected_event.set()
        disconnect_event.wait()
    disconnected_event.set()


@pytest.fixture
def local_address():
    local_ip = socket.gethostbyname('localhost')
    local_port = TEST_SOCKET_PORT
    yield PeerAddress(
        local_ip,
        local_port,
    )


@pytest.fixture
def inbound_socket_and_outbound_socket():

    # TODO: set up inbound and outbound sockets
    started = threading.Event()

    # Use futures
    with closing(socket.socket()) as listen_socket, \
            closing(socket.socket()) as peer_socket, \
            ThreadPoolExecutor(max_workers=2) as executor:
        inbound_future = executor.submit(
            accept_connections, listen_socket, started)
        outbound_future = executor.submit(
            make_connection, peer_socket, started)

        inbound_socket = inbound_future.result()
        print(inbound_socket)
        if isinstance(inbound_socket, Exception):
            raise inbound_socket
        outbound_socket = outbound_future.result()
        print(outbound_socket)

        yield inbound_socket, outbound_socket


@pytest.fixture
def inbound_socket(inbound_socket_and_outbound_socket):
    inbound_socket, _ = inbound_socket_and_outbound_socket
    yield inbound_socket


@pytest.fixture
def outbound_socket(inbound_socket_and_outbound_socket):
    _, outbound_socket = inbound_socket_and_outbound_socket
    yield outbound_socket


@pytest.fixture
def inbound_local_address():
    yield PeerAddress('inbound.com', 56789)


@pytest.fixture
def outbound_local_address():
    yield PeerAddress('outbound.com', 4321)


@pytest.fixture
def inbound_connection_manager(local_address):
    yield ConnectionManager(local_address)


@pytest.fixture
def outbound_connection_manager(local_address):
    yield ConnectionManager(local_address)


@pytest.fixture
def squeak_controller():
    return mock.Mock(spec=SqueakController)


def test_connect_peers(
        inbound_socket,
        outbound_socket,
        inbound_connection_manager,
        outbound_connection_manager,
        inbound_local_address,
        outbound_local_address,
        squeak_controller,
        caplog,
):
    import logging
    caplog.set_level(logging.INFO)
    inbound_q = queue.Queue()
    outbound_q = queue.Queue()

    assert inbound_socket is not None
    assert outbound_socket is not None

    assert len(inbound_connection_manager.peers) == 0
    assert len(outbound_connection_manager.peers) == 0

    inbound_connected_event = threading.Event()
    inbound_disconnect_event = threading.Event()
    inbound_disconnected_event = threading.Event()
    # Start the inbound connection in a thread.
    inbound_connection_thread = threading.Thread(
        target=start_connection,
        args=(
            inbound_connection_manager,
            inbound_connected_event,
            inbound_disconnect_event,
            inbound_disconnected_event,
            inbound_socket,
            outbound_local_address,
            False,
            squeak_controller,
            inbound_q,
        ))
    inbound_connection_thread.start()

    outbound_connected_event = threading.Event()
    outbound_disconnect_event = threading.Event()
    outbound_disconnected_event = threading.Event()
    # Start the outbound connection in a thread.
    outbound_connection_thread = threading.Thread(
        target=start_connection,
        args=(
            outbound_connection_manager,
            outbound_connected_event,
            outbound_disconnect_event,
            outbound_disconnected_event,
            outbound_socket,
            inbound_local_address,
            True,
            squeak_controller,
            outbound_q,
        ))
    outbound_connection_thread.start()

    # import time
    # time.sleep(5)
    # assert False

    # Wait for both sides of connection to be connected
    inbound_connected_event.wait()
    outbound_connected_event.wait()

    print('Opened connection.')
    assert len(inbound_connection_manager.peers) == 1
    assert len(outbound_connection_manager.peers) == 1

    inbound_disconnect_event.set()
    outbound_disconnect_event.set()

    inbound_disconnected_event.wait()
    outbound_disconnected_event.wait()

    print('Closed connection.')
    assert len(inbound_connection_manager.peers) == 0
    assert len(outbound_connection_manager.peers) == 0
