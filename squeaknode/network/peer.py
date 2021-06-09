import logging
import queue
import threading
import time
from io import BytesIO

from bitcoin.core.serialize import SerializationTruncationError
from bitcoin.net import CAddress
from squeak.messages import MsgSerializable

from squeaknode.core.peer_address import PeerAddress


MAX_MESSAGE_LEN = 1048576
SOCKET_READ_LEN = 1024
LAST_MESSAGE_TIMEOUT = 600
PING_TIMEOUT = 10
PING_INTERVAL = 60


logger = logging.getLogger(__name__)


class Peer(object):
    """Maintains the internal state of a peer connection.
    """

    def __init__(self, peer_socket, address, outgoing=False):
        time_now = int(time.time())
        self._peer_socket = peer_socket
        self._peer_socket_lock = threading.Lock()
        self._address = address
        self._outgoing = outgoing
        self._connect_time = time_now
        self._local_version = None
        self._remote_version = None
        self._last_msg_revc_time = None
        self._last_sent_ping_nonce = None
        self._last_sent_ping_time = None
        self._last_recv_ping_time = None
        self._recv_msg_queue = queue.Queue()

        self.handshake_complete = threading.Event()
        self.ping_started = threading.Event()
        self.ping_complete = threading.Event()
        self.stopped = threading.Event()

    @property
    def nVersion(self):
        remote_version = self._remote_version
        if remote_version:
            return remote_version.nVersion

    @property
    def address(self):
        return self._address

    @property
    def peer_address(self):
        ip, port = self._address
        return PeerAddress(
            host=ip,
            port=port,
        )

    @property
    def address_string(self):
        ip, port = self._address
        return '{}:{}'.format(ip, port)

    @property
    def ip(self):
        ip, _ = self._address
        return ip

    @property
    def port(self):
        _, port = self._address
        return port

    @property
    def caddress(self):
        ip, port = self._address
        caddress = CAddress()
        caddress.nTime = self.connect_time
        caddress.ip = ip
        caddress.port = port
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
    def is_handshake_complete(self):
        return self.handshake_complete.is_set()

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

    def recv_msg(self):
        """Read data from the peer socket, and yield messages as they are decoded.

        This method blocks when the socket has no data to read.
        """
        msg = self._recv_msg_queue.get()
        logger.debug('Received msg {} from {}'.format(msg, self))
        logger.info('Received msg {} from {}'.format(msg, self))
        return msg

    def stop(self):
        logger.info("Stopping peer: {}".format(self))
        self.stopped.set()

    def close(self):
        logger.info("closing peer socket: {}".format(self._peer_socket))
        if self._peer_socket:
            self._peer_socket.close()

    def send_msg(self, msg):
        logger.debug('Sending msg {} to {}'.format(msg, self))
        logger.info('Sending msg {} to {}'.format(msg, self))
        data = msg.to_bytes()
        with self._peer_socket_lock:
            self._peer_socket.send(data)

    def __enter__(self):
        logger.debug('Setting up peer {} ...'.format(self))
        msg_receiver = MessageReceiver(
            self._peer_socket, self._recv_msg_queue, self.stopped)
        threading.Thread(
            target=msg_receiver.recv_msgs,
            args=(),
        ).start()
        return self

    def __exit__(self, *exc):
        self.stop()
        logger.debug('Stopped peer {} ...'.format(self))

    def __repr__(self):
        return "Peer(%s)" % (self.address_string)


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

    def __init__(self, socket, queue, stopped_event):
        self.socket = socket
        self.queue = queue
        self.stopped_event = stopped_event
        self.decoder = MessageDecoder()

    def _recv_msgs(self):
        while True:
            recv_data = self.socket.recv(SOCKET_READ_LEN)
            if not recv_data:
                raise Exception('Peer disconnected')

            for msg in self.decoder.process_recv_data(recv_data):
                self.queue.put(msg)
                if self.stopped_event.is_set():
                    return

    def recv_msgs(self):
        try:
            self._recv_msgs()
        except Exception:
            self.stopped_event.set()
