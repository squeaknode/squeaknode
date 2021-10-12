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
import socket
import threading
import time
from io import BytesIO
from typing import Optional

from bitcoin.core.serialize import SerializationTruncationError
from bitcoin.net import CAddress
from squeak.core import CSqueak
from squeak.messages import msg_getsqueaks
from squeak.messages import msg_subscribe
from squeak.messages import msg_verack
from squeak.messages import msg_version
from squeak.messages import MsgSerializable
from squeak.net import CSqueakLocator

from squeaknode.core.crypto import generate_version_nonce
from squeaknode.core.interests import get_differential_squeaks
from squeaknode.core.interests import squeak_matches_interest
from squeaknode.core.peer_address import PeerAddress
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
        self._num_msgs_received = 0
        self._num_bytes_received = 0
        self._num_msgs_sent = 0
        self._num_bytes_sent = 0

        self._remote_subscription = None
        self._local_subscription = None

        self.msg_receiver = MessageReceiver(
            self._peer_socket,
        )
        self.received_msgs_iter = self.msg_receiver.recv_msgs()

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
    def remote_subscription(self):
        return self._remote_subscription

    @property
    def local_subscription(self):
        return self._local_subscription

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
        # TODO: Set the remote address ip
        # caddress.ip =
        caddress.port = self.remote_address.port
        return caddress

    @property
    def outgoing(self):
        return self._outgoing

    @property
    def connect_time(self):
        return self._connect_time

    @property
    def num_msgs_received(self):
        return self._num_msgs_received

    @property
    def num_bytes_received(self):
        return self._num_bytes_received

    @property
    def num_msgs_sent(self):
        return self._num_msgs_sent

    @property
    def num_bytes_sent(self):
        return self._num_bytes_sent

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
        try:
            msg = next(self.received_msgs_iter)
        except Exception:
            return None
        self.record_msg_received(msg)
        self.on_peer_updated()
        logger.info('Received msg {} from {}'.format(msg, self))
        return msg

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
                self.record_msg_sent(msg)
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
            raise Exception('Expected verack response: {}'.format(
                verack,
            ))

    def receive_version(self):
        remote_version = self.recv_msg()
        if not isinstance(remote_version, msg_version):
            raise Exception('Expected version message. Received: {}'.format(
                remote_version,
            ))
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

    def set_remote_subscription(self, locator: Optional[CSqueakLocator]):
        self._remote_subscription = locator

    def set_local_subscription(self, locator: Optional[CSqueakLocator]):
        self._local_subscription = locator

    def is_remote_subscribed(self, squeak: CSqueak):
        if self.remote_subscription is None:
            return False
        for interest in self.remote_subscription.vInterested:
            if squeak_matches_interest(squeak, interest):
                return True
        return False

    def update_local_subscription(self, locator: CSqueakLocator):
        assert len(locator.vInterested) <= 1
        if len(locator.vInterested) == 0:
            locator = None

        # Send the subscribe message
        subscribe_msg = msg_subscribe(
            locator=locator,
        )
        self.send_msg(subscribe_msg)

        # Send the getsqueaks messages for differential interests
        if locator is not None:
            for interest in self.get_differential_interests(locator):
                diff_locator = CSqueakLocator(
                    vInterested=[interest]
                )
                getsqueaks_msg = msg_getsqueaks(
                    locator=diff_locator,
                )
                self.send_msg(getsqueaks_msg)

        # Set the local subscription with the new value
        self.set_local_subscription(locator)

    def get_differential_interests(self, locator: CSqueakLocator):
        if self._local_subscription is None:
            yield locator.vInterested[0]
        else:
            new_interest = locator.vInterested[0]
            old_interest = self._local_subscription.vInterested[0]
            for interest in get_differential_squeaks(new_interest, old_interest):
                yield interest

    def on_peer_updated(self):
        logger.debug('on_peer_updated: {}'.format(self))
        self.peer_changed_listener.handle_new_item(self)

    def record_msg_received(self, msg):
        self._num_msgs_received += 1
        self._num_bytes_received += len(msg.to_bytes())
        self._last_msg_revc_time = time_now()

    def record_msg_sent(self, msg):
        if msg:
            self._num_msgs_sent += 1
            self._num_bytes_sent += len(msg.to_bytes())

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
    """Reads bytes from the socket and return decoded messages in an iterator.
    """

    def __init__(self, socket):
        self.socket = socket
        self.decoder = MessageDecoder()

    def recv_msgs(self):
        while True:
            try:
                recv_data = self.socket.recv(SOCKET_READ_LEN)
            except Exception:
                logger.error("Error in recv")
                return
            if not recv_data:
                logger.error("revc_data is None")
                return

            for msg in self.decoder.process_recv_data(recv_data):
                yield msg
