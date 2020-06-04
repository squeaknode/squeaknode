import codecs
import logging
import os

import grpc

import squeaknode.common.lnd_pb2 as ln
import squeaknode.common.lnd_pb2_grpc as lnrpc
from squeaknode.common.lightning_client import LightningClient


logger = logging.getLogger(__name__)


# Due to updated ECDSA generated tls.cert we need to let gprc know that
# we need to use that cipher suite otherwise there will be a handhsake
# error when we communicate with the lnd rpc server.
os.environ["GRPC_SSL_CIPHER_SUITES"] = 'HIGH+ECDSA'
os.environ["GRPC_VERBOSITY"] = 'DEBUG'


class LNDLightningClient(LightningClient):
    """Access a lightning deamon using RPC."""

    def __init__(
            self,
            host: str,
            port: int,
            network: str,
    ) -> None:
        url = '{}:{}'.format(host, port)
        tls_cert_path = '~/.lnd/tls.cert'
        macaroon_path = '~/.lnd/data/chain/bitcoin/{}/admin.macaroon'.format(network)

        # Lnd cert is at ~/.lnd/tls.cert on Linux and
        # ~/Library/Application Support/Lnd/tls.cert on Mac
        cert = open(os.path.expanduser(tls_cert_path), 'rb').read()
        creds = grpc.ssl_channel_credentials(cert)
        channel = grpc.secure_channel(url, creds)
        self.stub = lnrpc.LightningStub(channel)

        # Lnd admin macaroon is at ~/.lnd/data/chain/bitcoin/simnet/admin.macaroon on Linux and
        # ~/Library/Application Support/Lnd/data/chain/bitcoin/simnet/admin.macaroon on Mac
        with open(os.path.expanduser(macaroon_path), 'rb') as f:
            macaroon_bytes = f.read()
            self.macaroon = codecs.encode(macaroon_bytes, 'hex'
                                          )

    def get_wallet_balance(self):
        # Retrieve and display the wallet balance
        return self.stub.WalletBalance(ln.WalletBalanceRequest(), metadata=[('macaroon', self.macaroon)])
