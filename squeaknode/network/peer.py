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
import logging
import queue
import socket
import threading
import time
from io import BytesIO

from bitcoin.core.serialize import SerializationTruncationError
from bitcoin.net import CAddress
from squeak.messages import msg_verack
from squeak.messages import msg_version
from squeak.messages import MsgSerializable

from squeaknode.core.peer_address import PeerAddress
from squeaknode.core.util import generate_version_nonce
from squeaknode.network.util import time_now
from squeaknode.node.listener_subscription_client import EventListener


MAX_MESSAGE_LEN = 1048576
SOCKET_READ_LEN = 1024
LAST_MESSAGE_TIMEOUT = 600
PING_TIMEOUT = 10
PING_INTERVAL = 60

UPDATE_TIME_INTERVAL = 10
HANDSHAKE_VERSION = 70002


logger = logging.getLogger(__name__)


class Peer(object):
    """Maintains the internal state of a peer connection.
    """

    def __init__(
            self,
            peer_socket: socket.socket,
            local_address: PeerAddress,
            remote_address: PeerAddress,
            outgoing: bool,
            peer_changed_listener: EventListener,
    ):
        self._peer_socket = peer_socket
        self._peer_socket_lock = threading.Lock()
        self._local_address = local_address
        self._remote_address = remote_address
        self._outgoing = outgoing
        self._connect_time = 0
        self._local_version = None
        self._remote_version = None
        self._last_msg_revc_time = None
        self._last_sent_ping_nonce = None
        self._last_sent_ping_time = None
        self._last_recv_ping_time = None
        self._recv_msg_queue: queue.Queue = queue.Queue()

        self._subscription = None

        self.msg_receiver = MessageReceiver(
            self._peer_socket,
            self._recv_msg_queue,
        )
        self.peer_changed_listener = peer_changed_listener

    @property
    def nVersion(self):
        remote_version = self._remote_version
        if remote_version:
            return remote_version.nVersion

    @property
    def local_address(self):
        return self._local_address

    @property
    def remote_address(self):
        return self._remote_address

    @property
    def subscription(self):
        return self._subscription

    @property
    def local_caddress(self):
        caddress = CAddress()
        caddress.nTime = self.connect_time
        caddress.ip = self.local_address.host
        caddress.port = self.local_address.port
        return caddress

    @property
    def remote_caddress(self):
        caddress = CAddress()
        caddress.nTime = self.connect_time
        caddress.ip = socket.gethostbyname(self.remote_address.host)
        caddress.port = self.remote_address.port
        return caddress

    @property
    def outgoing(self):
        return self._outgoing

    @property
    def connect_time(self):
        return self._connect_time

    @property
    def local_version(self):
        return self._local_version

    @local_version.setter
    def local_version(self, local_version):
        self._local_version = local_version

    @property
    def remote_version(self):
        return self._remote_version

    @remote_version.setter
    def remote_version(self, remote_version):
        self._remote_version = remote_version

    @property
    def last_msg_revc_time(self):
        return self._last_msg_revc_time

    @property
    def last_sent_ping_time(self):
        return self._last_sent_ping_time

    def set_last_sent_ping(self, nonce, timestamp=None):
        timestamp = timestamp or time.time()
        self._last_sent_ping_nonce = nonce
        self._last_sent_ping_time = time.time()

    @property
    def last_recv_ping_time(self):
        return self._last_recv_ping_time

    def set_last_recv_ping(self, timestamp=None):
        timestamp = timestamp or time.time()
        self._last_recv_ping_time = timestamp

    # @property
    # def peer_state(self):
    #     return ConnectedPeer(
    #         peer_address=self.remote_address,
    #         connect_time_s=self.connect_time,
    #         outgoing=self.outgoing,
    #         sent_bytes=0,
    #         sent_messages=0,
    #         received_bytes=0,
    #         received_messages=0,
    #     )

    def recv_msg(self):
        """Read data from the peer socket, and yield messages as they are decoded.

        This method blocks when the socket has no data to read.
        """
        msg = self._recv_msg_queue.get()
        self.on_peer_updated()
        logger.info('Received msg {} from {}'.format(msg, self))
        return msg

    def recv_msgs(self):
        self.msg_receiver.recv_msgs()

    def stop(self):
        logger.info("Stopping peer socket: {}".format(self._peer_socket))
        try:
            self._peer_socket.shutdown(socket.SHUT_RDWR)
            self._peer_socket.stop()
        except Exception:
            pass
        finally:
            self.set_disconnected()
            self.on_peer_updated()

    def send_msg(self, msg):
        logger.info('Sending msg {} to {}'.format(msg, self))
        data = msg.to_bytes()
        try:
            with self._peer_socket_lock:
                self._peer_socket.send(data)
                self.on_peer_updated()
        except Exception:
            logger.info('Failed to send msg to {}'.format(self))
            self.stop()

    def send_version(self):
        local_version = self.version_pkt()
        self.local_version = local_version
        self.send_msg(local_version)
        verack = self.recv_msg()
        if not isinstance(verack, msg_verack):
            raise Exception('Wrong message type for verack response.')

    def receive_version(self):
        remote_version = self.recv_msg()
        if not isinstance(remote_version, msg_version):
            raise Exception('Wrong message type for version message.')
        self.remote_version = remote_version
        verack = msg_verack()
        self.send_msg(verack)

    def version_pkt(self):
        """Get the version message for this peer."""
        msg = msg_version()
        msg.nVersion = HANDSHAKE_VERSION
        msg.addrTo = self.remote_caddress
        msg.addrFrom = self.local_caddress
        msg.nNonce = generate_version_nonce()
        return msg

    def set_connected(self):
        self._connect_time = time_now()

    def set_disconnected(self):
        self._connect_time = None

    def set_subscription(self, subscription):
        self._subscription = subscription

    def on_peer_updated(self):
        logger.info('on_peer_updated: {}'.format(self))
        self.peer_changed_listener.handle_new_item(self)

    # def subscribe_peer_state(self, stopped):
    #     for result in self.peer_changed_listener.yield_items(stopped):
    #         yield result

    def __repr__(self):
        return "Peer(%s)" % (str(self.remote_address))


class MessageDecoder:
    """Handles the incoming binary data from a peer and buffers and decodes.
    """

    def __init__(self):
        self.recv_data_buffer = BytesIO()

    def process_recv_data(self, recv_data):
        data = self.read_data_buffer() + recv_data
        try:
            while data:
                self.set_data_buffer(data)
                msg = MsgSerializable.stream_deserialize(self.recv_data_buffer)
                if msg is None:
                    raise Exception('Invalid data')
                else:
                    yield msg
                    data = self.read_data_buffer()
        except SerializationTruncationError:
            self.set_data_buffer(data)

    def read_data_buffer(self):
        return self.recv_data_buffer.read()

    def set_data_buffer(self, data):
        if len(data) > MAX_MESSAGE_LEN:
            raise Exception('Message size too large')
        self.recv_data_buffer = BytesIO(data)


class MessageReceiver:
    """Reads bytes from the socket and puts messages in the receive queue.
    """

    def __init__(self, socket, queue):
        self.socket = socket
        self.queue = queue
        self.decoder = MessageDecoder()

    def _recv_msgs(self):
        while True:
            try:
                recv_data = self.socket.recv(SOCKET_READ_LEN)
            except Exception:
                logger.error("Error in recv")
                self.queue.put(None)
                raise Exception('Peer disconnected')
            if not recv_data:
                logger.error("revc_data is None")
                self.queue.put(None)
                raise Exception('Peer disconnected')

            for msg in self.decoder.process_recv_data(recv_data):
                self.queue.put(msg)

    def recv_msgs(self):
        try:
            self._recv_msgs()
        except Exception:
            logger.info('Failed to receive msg from {}'.format(self))
