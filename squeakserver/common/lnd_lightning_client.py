import codecs
import logging
import os

import grpc

from proto import lnd_pb2, lnd_pb2_grpc

logger = logging.getLogger(__name__)


# Due to updated ECDSA generated tls.cert we need to let gprc know that
# we need to use that cipher suite otherwise there will be a handhsake
# error when we communicate with the lnd rpc server.
os.environ["GRPC_SSL_CIPHER_SUITES"] = "HIGH+ECDSA"
# os.environ["GRPC_VERBOSITY"] = "DEBUG"


class LNDLightningClient:
    """Access a lightning deamon using RPC."""

    def __init__(
        self,
        host: str,
        port: int,
        tls_cert_path: str,
        macaroon_path: str,
    ) -> None:
        url = "{}:{}".format(host, port)

        # Lnd cert is at ~/.lnd/tls.cert on Linux and
        # ~/Library/Application Support/Lnd/tls.cert on Mac
        cert = open(os.path.expanduser(tls_cert_path), "rb").read()
        creds = grpc.ssl_channel_credentials(cert)
        channel = grpc.secure_channel(url, creds)
        self.stub = lnd_pb2_grpc.LightningStub(channel)

        # Lnd admin macaroon is at ~/.lnd/data/chain/bitcoin/simnet/admin.macaroon on Linux and
        # ~/Library/Application Support/Lnd/data/chain/bitcoin/simnet/admin.macaroon on Mac
        with open(os.path.expanduser(macaroon_path), "rb") as f:
            macaroon_bytes = f.read()
            self.macaroon = codecs.encode(macaroon_bytes, "hex")

    def get_wallet_balance(self):
        # Retrieve and display the wallet balance
        return self.stub.WalletBalance(
            lnd_pb2.WalletBalanceRequest(),
            metadata=[("macaroon", self.macaroon)],
        )

    def add_invoice(self, preimage, amount):
        """Create a new invoice with the given hash pre-image.

        args:
        preimage -- the preimage bytes used to create the invoice
        amount -- the value of the invoice
        """
        invoice = lnd_pb2.Invoice(
            r_preimage=preimage,
            value=amount,
        )
        return self.stub.AddInvoice(invoice, metadata=[("macaroon", self.macaroon)])

    def pay_invoice_sync(self, payment_request):
        """Pay an invoice with a given payment_request

        args:
        payment_request -- the payment_request as a string
        """
        send_payment_request = lnd_pb2.SendRequest(
            payment_request=payment_request,
        )
        return self.stub.SendPaymentSync(
            send_payment_request, metadata=[("macaroon", self.macaroon)]
        )

    def connect_peer(self, pubkey, host):
        """Connect to a lightning node peer.

        args:
        pubkey -- The identity pubkey of the Lightning node
        host -- The network location of the lightning node
        """
        lightning_address = lnd_pb2.LightningAddress(
            pubkey=pubkey,
            host=host,
        )
        connect_peer_request = lnd_pb2.ConnectPeerRequest(
            addr=lightning_address,
        )
        return self.stub.ConnectPeer(
            connect_peer_request, metadata=[("macaroon", self.macaroon)]
        )

    def get_info(self):
        """Get info about the lightning network node."""
        get_info_request = lnd_pb2.GetInfoRequest()
        return self.stub.GetInfo(
            get_info_request, metadata=[("macaroon", self.macaroon)]
        )

    def open_channel_sync(self, pubkey_str, local_amount):
        """Open a channel with a remote lightning node.

        args:
        pubkey (str) -- The identity pubkey of the Lightning node
        local_amount -- The number of satoshis the wallet should commit to the channel
        """
        open_channel_request = lnd_pb2.OpenChannelRequest(
            node_pubkey_string=pubkey_str,
            local_funding_amount=local_amount,
        )
        return self.stub.OpenChannelSync(
            open_channel_request, metadata=[("macaroon", self.macaroon)]
        )

    def list_channels(self):
        """List the channels"""
        list_channels_request = lnd_pb2.ListChannelsRequest()
        return self.stub.ListChannels(
            list_channels_request, metadata=[("macaroon", self.macaroon)]
        )

    def list_peers(self):
        """List the peers"""
        list_peers_request = lnd_pb2.ListPeersRequest()
        return self.stub.ListPeers(
            list_peers_request, metadata=[("macaroon", self.macaroon)]
        )

    def open_channel(self, pubkey, local_amount):
        """Open a channel

        args:
        pubkey (bytes) -- The identity pubkey of the Lightning node
        local_amount -- The number of satoshis the wallet should commit to the channel
        """
        open_channel_request = lnd_pb2.OpenChannelRequest(
            node_pubkey=pubkey,
            local_funding_amount=local_amount,
        )
        return self.stub.OpenChannel(
            open_channel_request, metadata=[("macaroon", self.macaroon)]
        )

    def close_channel(self, channel_point):
        """Close a channel

        args:
        channel_point (str) -- The outpoint (txid:index) of the funding transaction.
        """
        close_channel_request = lnd_pb2.CloseChannelRequest(
            channel_point=channel_point,
        )
        return self.stub.CloseChannel(
            close_channel_request, metadata=[("macaroon", self.macaroon)]
        )

    def decode_pay_req(self, payment_request):
        """Decode a payment request

        args:
        pay_req (str) -- The payment request string
        """
        decode_pay_req_request = lnd_pb2.PayReqString(
            pay_req=payment_request,
        )
        return self.stub.DecodePayReq(
            decode_pay_req_request, metadata=[("macaroon", self.macaroon)]
        )

    def new_address(self, address_type):
        # NewAddress creates a new address under control of the local wallet.
        new_address_request = lnd_pb2.NewAddressRequest(
            type=address_type,
        )
        return self.stub.NewAddress(
            new_address_request,
            metadata=[("macaroon", self.macaroon)],
        )

    def list_channels(self):
        # NewAddress creates a new address under control of the local wallet.
        list_channels_request = lnd_pb2.ListChannelsRequest()
        return self.stub.ListChannels(
            list_channels_request,
            metadata=[("macaroon", self.macaroon)],
        )
