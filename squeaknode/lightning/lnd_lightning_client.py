import codecs
import logging
import os

import grpc

from proto import lnd_pb2
from proto import lnd_pb2_grpc

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
        cert_creds = grpc.ssl_channel_credentials(cert)

        # Lnd admin macaroon is at ~/.lnd/data/chain/bitcoin/simnet/admin.macaroon on Linux and
        # ~/Library/Application Support/Lnd/data/chain/bitcoin/simnet/admin.macaroon on Mac
        with open(os.path.expanduser(macaroon_path), "rb") as f:
            macaroon_bytes = f.read()
            macaroon = codecs.encode(macaroon_bytes, "hex")
            self.macaroon = codecs.encode(macaroon_bytes, "hex")

        def metadata_callback(context, callback):
            # for more info see grpc docs
            callback([("macaroon", macaroon)], None)

        # now build meta data credentials
        auth_creds = grpc.metadata_call_credentials(metadata_callback)

        # combine the cert credentials and the macaroon auth credentials
        # such that every call is properly encrypted and authenticated
        combined_creds = grpc.composite_channel_credentials(
            cert_creds, auth_creds)

        # finally pass in the combined credentials when creating a channel
        channel = grpc.secure_channel(url, combined_creds)
        self.stub = lnd_pb2_grpc.LightningStub(channel)

    def get_wallet_balance(self):
        # Retrieve and display the wallet balance
        request = lnd_pb2.WalletBalanceRequest()
        return self.stub.WalletBalance(request)

    def add_invoice(self, preimage, amount_msat):
        """Create a new invoice with the given hash pre-image.

        args:
        preimage -- the preimage bytes used to create the invoice
        amount -- the value of the invoice
        """
        invoice = lnd_pb2.Invoice(
            r_preimage=preimage,
            value_msat=amount_msat,
        )
        return self.stub.AddInvoice(invoice)

    def pay_invoice_sync(self, payment_request):
        """Pay an invoice with a given payment_request

        args:
        payment_request -- the payment_request as a string
        """
        send_payment_request = lnd_pb2.SendRequest(
            payment_request=payment_request,
        )
        return self.stub.SendPaymentSync(send_payment_request)

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
        return self.stub.ConnectPeer(connect_peer_request)

    def disconnect_peer(self, pubkey):
        """Disconnect a lightning node peer.

        args:
        pubkey -- The identity pubkey of the Lightning node
        """
        disconnect_peer_request = lnd_pb2.DisconnectPeerRequest(
            pub_key=pubkey,
        )
        return self.stub.DisconnectPeer(
            disconnect_peer_request,
        )

    def get_info(self):
        """Get info about the lightning network node."""
        get_info_request = lnd_pb2.GetInfoRequest()
        return self.stub.GetInfo(
            get_info_request,
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
            open_channel_request,
        )

    def list_channels(self):
        """List the channels"""
        list_channels_request = lnd_pb2.ListChannelsRequest()
        return self.stub.ListChannels(
            list_channels_request,
        )

    def pending_channels(self):
        """List the pending channels"""
        pending_channels_request = lnd_pb2.PendingChannelsRequest()
        return self.stub.PendingChannels(
            pending_channels_request,
        )

    def list_peers(self):
        """List the peers"""
        list_peers_request = lnd_pb2.ListPeersRequest()
        return self.stub.ListPeers(
            list_peers_request,
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
            open_channel_request,
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
            close_channel_request,
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
            decode_pay_req_request,
        )

    def new_address(self, address_type):
        # NewAddress creates a new address under control of the local wallet.
        new_address_request = lnd_pb2.NewAddressRequest(
            type=address_type,
        )
        return self.stub.NewAddress(
            new_address_request,
        )

    def subscribe_channel_events(self):
        subscribe_channel_events_request = lnd_pb2.ChannelEventSubscription()
        return self.stub.SubscribeChannelEvents(
            subscribe_channel_events_request,
        )

    def get_transactions(self):
        # Get transactions
        get_transactions_request = lnd_pb2.GetTransactionsRequest()
        return self.stub.GetTransactions(
            get_transactions_request,
        )

    def send_coins(self, addr, amount):
        send_coins_request = lnd_pb2.SendCoinsRequest(
            addr=addr,
            amount=amount,
        )
        return self.stub.SendCoins(
            send_coins_request,
        )

    def subscribe_invoices(self, settle_index):
        subscribe_invoices_request = lnd_pb2.InvoiceSubscription(
            settle_index=settle_index,
        )
        return self.stub.SubscribeInvoices(
            subscribe_invoices_request,
        )

    def lookup_invoice(self, r_hash_str):
        """Look up an invoice.

        args:
        r_hash_str -- The hex-encoded payment hash of the invoice to be looked up.
        """
        payment_hash = lnd_pb2.PaymentHash(
            r_hash_str=r_hash_str,
        )
        return self.stub.LookupInvoice(payment_hash)
