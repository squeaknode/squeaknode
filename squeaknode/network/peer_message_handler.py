import logging

from squeak.messages import msg_addr
from squeak.messages import msg_getdata
from squeak.messages import msg_inv
from squeak.messages import msg_notfound
from squeak.messages import msg_offer
from squeak.messages import msg_ping
from squeak.messages import msg_pong
from squeak.messages import msg_squeak
from squeak.net import CInv

from squeaknode.core.offer import Offer
from squeaknode.core.util import generate_ping_nonce
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

    def initiate_ping(self):
        """Send a ping message and expect a pong response."""
        nonce = generate_ping_nonce()
        ping = msg_ping()
        ping.nonce = nonce
        self.peer.send_msg(ping)
        self.peer.set_last_sent_ping(nonce)

    def handle_msgs(self):
        """Handles messages from the peer if there are any available.

        This method blocks when the peer has not sent any messages.
        """
        logger.info('Started handling connected messages...')
        msg = self.peer.recv_msg()
        while msg is not None:
            self.handle_peer_message(msg)
            msg = self.peer.recv_msg()
        logger.info('Finished handling connected messages...')

    def handle_peer_message(self, msg):
        """Handle messages from a peer with completed handshake."""

        # # Only allow version and verack messages before handshake is complete.
        # if not self.peer.is_handshake_complete and msg.command not in [
        #         b'version',
        #         b'verack',
        # ]:
        #     raise Exception(
        #         'Received non-handshake message from un-handshaked peer.')

        # if msg.command == b'version':
        #     self.handle_version(msg)
        # if msg.command == b'verack':
        #     self.handle_verack(msg)

        if msg.command == b'ping':
            self.handle_ping(msg)
        if msg.command == b'pong':
            self.handle_pong(msg)
        if msg.command == b'addr':
            self.handle_addr(msg)
        if msg.command == b'getaddr':
            self.handle_getaddr(msg)
        if msg.command == b'inv':
            self.handle_inv(msg)
        if msg.command == b'getsqueaks':
            self.handle_getsqueaks(msg)
        if msg.command == b'squeak':
            self.handle_squeak(msg)
        if msg.command == b'getdata':
            self.handle_getdata(msg)
        if msg.command == b'notfound':
            self.handle_notfound(msg)
        if msg.command == b'offer':
            self.handle_offer(msg)

    def handle_ping(self, msg):
        nonce = msg.nonce
        pong = msg_pong()
        pong.nonce = nonce
        self.peer.set_last_recv_ping()
        self.peer.send_msg(pong)

    def handle_pong(self, msg):
        self.peer.set_pong_response(msg.nonce)

    def handle_addr(self, msg):
        for addr in msg.addrs:
            self.peer_server.connect_address((addr.ip, addr.port))

    def handle_getaddr(self, msg):
        peers = self.node.get_peers()
        addresses = [peer.caddress for peer in peers
                     if peer.outgoing]
        addr_msg = msg_addr(addrs=addresses)
        self.peer.send_msg(addr_msg)

    def handle_inv(self, msg):
        invs = msg.inv
        unknown_invs = self.squeak_controller.filter_known_invs(invs)
        if unknown_invs:
            getdata_msg = msg_getdata(inv=unknown_invs)
            self.peer.send_msg(getdata_msg)

    def handle_getdata(self, msg):
        invs = msg.inv
        not_found = []
        for inv in invs:
            if inv.type == 1:
                squeak = self.squeak_controller.get_squeak(inv.hash)
                if squeak is None:
                    not_found.append(inv)
                else:
                    squeak.ClearDecryptionKey()
                    squeak_msg = msg_squeak(squeak=squeak)
                    self.peer.send_msg(squeak_msg)
            if inv.type == 2:
                offer = self.squeak_controller.get_buy_offer(
                    squeak_hash=inv.hash,
                    client_address=self.peer.peer_address,
                )
                if offer is None:
                    not_found.append(inv)
                else:
                    offer_msg = msg_offer(
                        hashSqk=inv.hash,
                        nonce=offer.nonce,
                        strPaymentInfo=offer.payment_request.encode('utf-8'),
                        host=offer.host.encode('utf-8'),
                        port=offer.port,
                    )
                    self.peer.send_msg(offer_msg)
        if not_found:
            notfound_msg = msg_notfound(inv=not_found)
            self.peer.send_msg(notfound_msg)

    def handle_notfound(self, msg):
        pass

    def handle_getsqueaks(self, msg):
        # TODO: Maybe combine all invs into a single send_msg.
        for interest in msg.locator.vInterested:
            min_block = interest.nMinBlockHeight if interest.nMinBlockHeight != -1 else None
            max_block = interest.nMaxBlockHeight if interest.nMaxBlockHeight != -1 else None
            reply_to_hash = interest.hashReplySqk if interest.hashReplySqk != EMPTY_HASH else None
            squeak_hashes = self.squeak_controller.lookup_squeaks_for_interest(
                address=str(interest.address),
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

    def handle_squeak(self, msg):
        squeak = msg.squeak
        # TODO: check if interested before saving.
        self.squeak_controller.save_squeak(squeak)

    def handle_offer(self, msg):
        # TODO: check if interested before saving.
        offer = Offer(
            squeak_hash=msg.hashSqk,
            nonce=msg.nonce,
            payment_request=msg.strPaymentInfo.decode('utf-8'),
            host=msg.host.decode('utf-8'),
            port=msg.port,
        )
        squeak = self.squeak_controller.get_squeak(offer.squeak_hash)
        if squeak is not None and not squeak.HasDecryptionKey():
            decoded_offer = self.squeak_controller.get_offer(
                squeak=squeak,
                offer=offer,
                peer_address=self.peer.peer_address,
            )
            self.squeak_controller.save_offer(decoded_offer)
