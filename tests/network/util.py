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
import socket
import threading
from concurrent.futures import ThreadPoolExecutor
from contextlib import closing


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


def yield_inbound_socket_and_outbound_socket():
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
