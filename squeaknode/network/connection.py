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
import threading

from squeak.messages import msg_addr
from squeak.messages import msg_getaddr
from squeak.messages import msg_getdata
from squeak.messages import msg_inv
from squeak.messages import msg_notfound
from squeak.messages import msg_ping
from squeak.messages import msg_pong
from squeak.messages import MSG_SECRET_KEY
from squeak.messages import MSG_SQUEAK
from squeak.messages import msg_squeak
from squeak.net import CInterested
from squeak.net import CInv

from squeaknode.core.crypto import generate_ping_nonce
from squeaknode.core.offer import Offer
from squeaknode.network.download_handler import DownloadHandler
from squeaknode.network.peer import Peer
from squeaknode.node.squeak_controller import SqueakController


logger = logging.getLogger(__name__)


EMPTY_HASH = b'\x00' * 32
HANDSHAKE_TIMEOUT = 30
PING_TIMEOUT = 60
PONG_TIMEOUT = 30


class Connection(object):
    """Handles lifecycle of a connection to a peer.
    """

    def __init__(self, peer: Peer, squeak_controller: SqueakController):
        self.peer = peer
        self.squeak_controller = squeak_controller
        self.handshake_timer = HandshakeTimer(self)
        self.ping_timer = PingTimer(self)
        self.pong_timer = PongTimer(self)
        self.download_handler = DownloadHandler(self.squeak_controller)

    def handshake(self):
        """Do a handshake with a peer.
        """
        self.handshake_timer.start_timer()

        if self.peer.outgoing:
            self.peer.send_version()
        self.peer.receive_version()
        if not self.peer.outgoing:
            self.peer.send_version()

        self.peer.set_connected()
        self.handshake_timer.cancel()
        logger.debug("HANDSHAKE COMPLETE-----------")

    def shutdown(self):
        logger.info("Peer shutting down...")
        self.peer.stop()
        self.handshake_timer.cancel()
        self.ping_timer.cancel()
        self.pong_timer.cancel()

    def handle_connection(self):
        try:
            self.initial_sync()
            self.handle_msgs()
        except Exception:
            logger.exception("Error in handle_connection")
        finally:
            self.shutdown()
            # self._stopped.set()

    def initial_sync(self):
        self.send_ping()
        self.update_addrs()
        self.update_subscription()

    def send_ping(self):
        ping_msg = msg_ping()
        ping_msg.nonce = generate_ping_nonce()
        self.pong_timer.start_timer(ping_msg.nonce)
        self.peer.send_msg(ping_msg)

    def start_ping_timer(self):
        self.ping_timer.start_timer()

    def update_subscription(self):
        locator = self.squeak_controller.get_interested_locator()
        self.peer.update_local_subscription(locator)

    def update_addrs(self):
        getaddr_msg = msg_getaddr()
        self.peer.send_msg(getaddr_msg)

    def handle_msgs(self):
        """Handles messages from the peer if there are any available.

        This method blocks when the peer has not sent any messages.
        """
        msg = self.peer.recv_msg()
        while msg is not None:
            self.handle_peer_message(msg)
            msg = self.peer.recv_msg()
        logger.info("Finished handle_msgs")

    def handle_peer_message(self, msg):
        """Handle messages from a peer with completed handshake."""
        if msg.command == b'ping':
            self.handle_ping(msg)
        elif msg.command == b'pong':
            self.handle_pong(msg)
        elif msg.command == b'addr':
            self.handle_addr(msg)
        elif msg.command == b'getaddr':
            self.handle_getaddr(msg)
        elif msg.command == b'inv':
            self.handle_inv(msg)
        elif msg.command == b'getsqueaks':
            self.handle_getsqueaks(msg)
        elif msg.command == b'squeak':
            self.handle_squeak(msg)
        elif msg.command == b'getdata':
            self.handle_getdata(msg)
        elif msg.command == b'notfound':
            self.handle_notfound(msg)
        elif msg.command == b'offer':
            self.handle_offer(msg)
        elif msg.command == b'secretkey':
            self.handle_secret_key(msg)
        elif msg.command == b'subscribe':
            self.handle_subscribe(msg)
        else:
            raise Exception("Unrecognized message: {}".format(
                msg.command
            ))

    def handle_ping(self, msg):
        nonce = msg.nonce
        pong = msg_pong()
        pong.nonce = nonce
        self.peer.set_last_recv_ping()
        self.peer.send_msg(pong)

    def handle_pong(self, msg):
        nonce = msg.nonce
        self.pong_timer.stop_timer(nonce)

    def handle_addr(self, msg):
        # TODO: Save new address in table.
        for addr in msg.addrs:
            pass

    def handle_getaddr(self, msg):
        # TODO: Get known peers from table in database.
        addr_msg = msg_addr(addrs=[])
        self.peer.send_msg(addr_msg)

    def handle_inv(self, msg):
        invs = msg.inv
        unknown_squeak_invs = [
            inv for inv in invs
            if inv.type == MSG_SQUEAK
            and self.squeak_controller.get_squeak(inv.hash) is None
        ]
        unknown_secret_key_invs = [
            inv for inv in invs
            if inv.type == MSG_SECRET_KEY
            and self.squeak_controller.get_squeak(inv.hash) is not None
            and self.squeak_controller.get_squeak_secret_key(inv.hash) is None
        ]
        unknown_invs = unknown_squeak_invs + unknown_secret_key_invs
        if unknown_invs:
            getdata_msg = msg_getdata(inv=unknown_invs)
            self.peer.send_msg(getdata_msg)

    def handle_getdata(self, msg):
        invs = msg.inv
        not_found = []
        for inv in invs:
            reply_msg = self._get_inv_reply(inv)
            if reply_msg is not None:
                self.peer.send_msg(reply_msg)
            else:
                not_found.append(inv)
        if not_found:
            notfound_msg = msg_notfound(inv=not_found)
            self.peer.send_msg(notfound_msg)

    def handle_notfound(self, msg):
        pass

    def handle_getsqueaks(self, msg):
        self._send_reply_invs(msg.locator)

    def handle_squeak(self, msg):
        squeak = msg.squeak
        self.download_handler.handle_squeak(squeak)

    def handle_offer(self, msg):
        offer = Offer(
            squeak_hash=msg.hashSqk,
            nonce=msg.nonce,
            payment_request=msg.strPaymentInfo.decode('utf-8'),
            host=msg.host.decode('utf-8'),
            port=msg.port,
        )
        self.download_handler.handle_offer(
            offer,
            self.peer.remote_address,
        )

    def handle_secret_key(self, msg):
        self.squeak_controller.unlock_squeak(
            msg.hashSqk,
            msg.secretKey,
        )

    def handle_subscribe(self, msg):
        if msg.protover < 60003:
            self._send_reply_invs(msg.locator)
        self.peer.set_remote_subscription(msg.locator)

    def _send_reply_invs(self, locator):
        for interest in locator.vInterested:
            squeak_hashes = self._get_local_squeaks(interest)
            secret_key_hashes = self._get_local_secret_keys(interest)
            squeak_invs = [
                CInv(type=MSG_SQUEAK, hash=squeak_hash)
                for squeak_hash in squeak_hashes]
            secret_key_invs = [
                CInv(type=MSG_SECRET_KEY, hash=squeak_hash)
                for squeak_hash in secret_key_hashes]
            invs = squeak_invs + secret_key_invs
            if invs:
                inv_msg = msg_inv(inv=invs)
                self.peer.send_msg(inv_msg)

    def _get_local_squeaks(self, interest: CInterested):
        min_block = interest.nMinBlockHeight if interest.nMinBlockHeight != -1 else None
        max_block = interest.nMaxBlockHeight if interest.nMaxBlockHeight != -1 else None
        reply_to_hash = interest.hashReplySqk if interest.hashReplySqk != EMPTY_HASH else None
        return self.squeak_controller.lookup_squeaks(
            public_keys=interest.pubkeys,
            min_block=min_block,
            max_block=max_block,
            reply_to_hash=reply_to_hash,
        )

    def _get_local_secret_keys(self, interest: CInterested):
        min_block = interest.nMinBlockHeight if interest.nMinBlockHeight != -1 else None
        max_block = interest.nMaxBlockHeight if interest.nMaxBlockHeight != -1 else None
        reply_to_hash = interest.hashReplySqk if interest.hashReplySqk != EMPTY_HASH else None
        return self.squeak_controller.lookup_secret_keys(
            public_keys=interest.pubkeys,
            min_block=min_block,
            max_block=max_block,
            reply_to_hash=reply_to_hash,
        )

    def _get_inv_reply(self, inv):
        if inv.type == MSG_SQUEAK:
            return self._get_inv_reply_for_squeak(inv)
        if inv.type == MSG_SECRET_KEY:
            return self._get_inv_reply_for_secret_key(inv)

    def _get_inv_reply_for_squeak(self, inv):
        squeak = self.squeak_controller.get_squeak(inv.hash)
        if squeak is not None:
            return msg_squeak(squeak=squeak)

    def _get_inv_reply_for_secret_key(self, inv):
        resp = self.squeak_controller.get_secret_key_reply(
            inv.hash,
            self.peer.remote_address,
        )
        if resp is None:
            return None
        return resp.get_msg()


class HandshakeTimer:
    """Stop the peer if handshake is not complete before timeout.
    """

    def __init__(self, connection: Connection):
        self.connection = connection
        self.timer = None
        self._lock = threading.Lock()

    def start_timer(self):
        with self._lock:
            self.timer = threading.Timer(
                HANDSHAKE_TIMEOUT,
                self.shutdown,
            )
            self.timer.name = "handshake_timer_thread_{}".format(
                self.connection.peer)
            self.timer.start()

    def cancel(self):
        logger.debug("Cancelling handshake timer.")
        with self._lock:
            if self.timer:
                self.timer.cancel()

    def shutdown(self):
        logger.info("Shutdown connection triggered by handshake timer.")
        self.connection.shutdown()


class PingTimer:
    """Send a ping message when the timer expires.
    """

    def __init__(self, connection: Connection):
        self.connection = connection
        self.timer = None
        self._lock = threading.Lock()

    def start_timer(self):
        logger.debug("Starting ping timer.")
        with self._lock:
            # Cancel the existing timer.
            if self.timer:
                self.timer.cancel()

            # Start a new timer.
            self.timer = threading.Timer(
                PING_TIMEOUT,
                self.send_ping,
            )
            self.timer.name = "ping_timer_thread_{}".format(
                self.connection.peer)
            self.timer.start()

    def cancel(self):
        logger.debug("Cancelling ping timer.")
        with self._lock:
            if self.timer:
                self.timer.cancel()

    def send_ping(self):
        logger.debug("Sending ping triggered by timer.")
        self.connection.send_ping()


class PongTimer:
    """Shut down the connection when the timer expires.
    """

    def __init__(self, connection: Connection):
        self.connection = connection
        self.timer = None
        self.expected_nonce = None
        self._lock = threading.Lock()

    def start_timer(self, nonce):
        logger.debug("Starting pong timer.")
        with self._lock:
            # Cancel the existing timer.
            if self.timer:
                return

            # Start a new timer.
            self.expected_nonce = nonce
            self.timer = threading.Timer(
                PONG_TIMEOUT,
                self.shutdown,
            )
            self.timer.name = "pong_timer_thread_{}".format(
                self.connection.peer)
            self.timer.start()

    def stop_timer(self, nonce):
        logger.debug("Stopping pong timer.")
        with self._lock:
            if nonce != self.expected_nonce:
                self.shutdown()

            # Cancel the existing timer.
            if self.timer:
                self.timer.cancel()
                self.timer = None
                self.expected_nonce = None

            # Start a new ping timer.
            self.start_ping_timer()

    def cancel(self):
        logger.debug("Cancelling pong timer.")
        with self._lock:
            if self.timer:
                self.timer.cancel()

    def shutdown(self):
        logger.info("Shutdown connection triggered by pong timer.")
        self.connection.shutdown()

    def start_ping_timer(self):
        logger.debug("Starting ping timer triggered by pong response.")
        self.connection.start_ping_timer()
