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

from squeak.messages import msg_addr
from squeak.messages import msg_getdata
from squeak.messages import msg_inv
from squeak.messages import msg_notfound
from squeak.messages import msg_offer
from squeak.messages import msg_pong
from squeak.messages import msg_secretkey
from squeak.messages import msg_squeak
from squeak.net import CInv

from squeaknode.core.offer import Offer
from squeaknode.core.peer_address import PeerAddress
from squeaknode.node.squeak_controller import SqueakController


logger = logging.getLogger(__name__)

EMPTY_HASH = b'\x00' * 32


class PeerMessageHandler:
    """Handles incoming messages from peers.
    """

    def __init__(
            self,
            peer,
            squeak_controller: SqueakController,
    ):
        self.peer = peer
        self.squeak_controller = squeak_controller

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
        self.peer.set_pong_response(msg.nonce)

    def handle_addr(self, msg):
        # TODO: Save new address in table rather than connecting.
        for addr in msg.addrs:
            peer_address = PeerAddress(
                host=addr.ip,
                port=addr.port,
            )
            self.squeak_controller.connect_peer(peer_address)

    def handle_getaddr(self, msg):
        # TODO: Get known peers from table in database.
        peers = self.squeak_controller.get_connected_peers()
        addresses = [
            peer.remote_caddress for peer in peers
            if peer.remote_caddress != self.peer.remote_caddress
        ]
        addr_msg = msg_addr(addrs=addresses)
        self.peer.send_msg(addr_msg)

    def handle_inv(self, msg):
        invs = msg.inv
        unknown_invs = [
            inv for inv in invs
            if inv.type == 1 and self.squeak_controller.get_squeak(inv.hash) is None
        ]
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
        self.squeak_controller.save_received_squeak(squeak)

    def handle_offer(self, msg):
        offer = Offer(
            squeak_hash=msg.hashSqk,
            nonce=msg.nonce,
            payment_request=msg.strPaymentInfo.decode('utf-8'),
            host=msg.host.decode('utf-8'),
            port=msg.port,
        )
        self.squeak_controller.save_received_offer(
            offer,
            self.peer.remote_address,
        )

    def handle_secret_key(self, msg):
        self.squeak_controller.unlock_squeak(
            msg.hashSqk,
            msg.secretKey,
        )

    def handle_subscribe(self, msg):
        self._send_reply_invs(msg.locator)
        self.peer.set_subscription(msg)

    def _send_reply_invs(self, locator):
        # TODO: Maybe combine all invs into a single send_msg.
        for interest in locator.vInterested:
            min_block = interest.nMinBlockHeight if interest.nMinBlockHeight != -1 else None
            max_block = interest.nMaxBlockHeight if interest.nMaxBlockHeight != -1 else None
            reply_to_hash = interest.hashReplySqk if interest.hashReplySqk != EMPTY_HASH else None
            squeak_hashes = self.squeak_controller.lookup_squeaks_for_interest(
                address=[str(address) for address in interest.addresses],
                min_block=min_block,
                max_block=max_block,
                reply_to_hash=reply_to_hash,
            )
            invs = [
                CInv(type=1, hash=squeak_hash)
                for squeak_hash in squeak_hashes]
            if invs:
                inv_msg = msg_inv(inv=invs)
                self.peer.send_msg(inv_msg)

    def _get_inv_reply(self, inv):
        if inv.type == 1:
            return self._get_inv_reply_for_squeak(inv)
        if inv.type == 2:
            return self._get_inv_reply_for_secret_key(inv)

    def _get_inv_reply_for_squeak(self, inv):
        squeak = self.squeak_controller.get_squeak(inv.hash)
        if squeak is not None:
            return msg_squeak(squeak=squeak)

    def _get_inv_reply_for_secret_key(self, inv):
        resp = self.squeak_controller.get_offer_or_secret_key(
            inv.hash,
            self.peer.remote_address,
        )
        if resp is None:
            return None
        elif type(resp) is bytes:
            return msg_secretkey(
                hashSqk=inv.hash,
                secretKey=resp,
            )
        elif type(resp) is Offer:
            return msg_offer(
                hashSqk=inv.hash,
                nonce=resp.nonce,
                strPaymentInfo=resp.payment_request.encode(
                    'utf-8'),
                host=resp.host.encode('utf-8'),
                port=resp.port,
            )
