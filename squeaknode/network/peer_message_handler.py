import logging

from squeak.messages import msg_addr
from squeak.messages import msg_getdata
from squeak.messages import msg_inv
from squeak.messages import msg_notfound
from squeak.messages import msg_ping
from squeak.messages import msg_pong
from squeak.messages import msg_squeak
from squeak.net import CInv
from squeakclient.squeaknode.util import generate_nonce


logger = logging.getLogger(__name__)


class PeerMessageHandler:
    """Handles incoming messages from peers.
    """

    def __init__(self, peer, node):
        self.peer = peer
        self.node = node

    def initiate_ping(self):
        """Send a ping message and expect a pong response."""
        nonce = generate_nonce()
        ping = msg_ping()
        ping.nonce = nonce
        self.peer.send_msg(ping)
        self.peer.set_last_sent_ping(nonce)

    def handle_msgs(self):
        """Handles messages from the peer if there are any available.

        This method blocks when the peer has not sent any messages.
        """
        while True:
            msg = self.peer.recv_msg()
            self.handle_peer_message(msg)

    def handle_peer_message(self, msg):
        """Handle messages from a peer with completed handshake."""

        # Only allow version and verack messages before handshake is complete.
        if not self.peer.is_handshake_complete and msg.command not in [
                b'version',
                b'verack',
        ]:
            raise Exception(
                'Received non-handshake message from un-handshaked peer.')

        if msg.command == b'version':
            self.handle_version(msg)
        if msg.command == b'verack':
            self.handle_verack(msg)
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
        saved_hashes = set(self.squeaks_access.get_squeak_hashes())
        received_hashes = set([inv.hash
                               for inv in invs
                               if inv.type == 1])
        new_hashes = received_hashes - saved_hashes

        new_invs = [CInv(type=1, hash=hash)
                    for hash in new_hashes]
        getdata_msg = msg_getdata(inv=new_invs)
        self.peer.send_msg(getdata_msg)

    def handle_getdata(self, msg):
        invs = msg.inv
        not_found = []
        for inv in invs:
            if inv.type == 1:
                squeak = self.squeaks_access.get_squeak(inv.hash)
                if squeak:
                    squeak_msg = msg_squeak(squeak=squeak)
                    self.peer.send_msg(squeak_msg)
                else:
                    not_found.append(inv)
        notfound_msg = msg_notfound(inv=not_found)
        self.peer.send_msg(notfound_msg)

    def handle_notfound(self, msg):
        pass

    def handle_getsqueaks(self, msg):
        locator = msg.locator
        squeaks = self.squeaks_access.get_squeaks_by_locator(locator)
        invs = [CInv(type=1, hash=squeak.GetHash())
                for squeak in squeaks]
        inv_msg = msg_inv(inv=invs)
        self.peer.send_msg(inv_msg)

    def handle_squeak(self, msg):
        # TODO: If squeak is interesting, respond with getoffer msg.
        squeak = msg.squeak
        self.squeaks_access.add_squeak(squeak)

    def handle_getoffer(self, msg):
        # Respond with offer msg.
        pass

    def handle_offer(self, msg):
        # Respond with getinvoice.
        pass

    def handle_getinvoice(self, msg):
        # Respond with invoice.
        pass

    def handle_invoice(self, msg):
        # Pay the invoice, and then respond with getfulfill.
        pass

    def handle_getfulfill(self, msg):
        # Check if invoice is paid, and then respond with fulfill.
        pass

    def handle_fulfill(self, msg):
        # Decrypt the squeak content, and save it in squeak store.
        pass
