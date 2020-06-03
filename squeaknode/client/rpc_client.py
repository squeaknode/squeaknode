import logging

import grpc

from squeaknode.common.rpc import squeak_server_pb2
from squeaknode.common.rpc import squeak_server_pb2_grpc

from squeak.core.signing import CSigningKey
from squeak.core.signing import CSqueakAddress

from squeaknode.client.squeak_store import SqueakStore
from squeaknode.common.blockchain_client import BlockchainClient
from squeaknode.common.lightning_client import LightningClient
from squeaknode.common.squeak_maker import SqueakMaker
from squeaknode.client.db import SQLiteDBFactory
from squeaknode.client.hub_store import HubStore


logger = logging.getLogger(__name__)


class RPCClient(object):
    """Does RPC commands on the server.
    """

    def __init__(
            self,
            host: str,
            port: int,
    ) -> None:
        self.host = host
        self.port = port
        logger.info('Created rpc client with host: {} and port {}'.format(host, port))

    def upload_squeak(self, squeak):
        squeak_hash = squeak.GetHash()
        logger.info("Upload the squeak here.")

        # Make the rpc request to the server.
        #channel = grpc.insecure_channel('localhost:50051')
        # channel = grpc.insecure_channel('{}:{}'.format(self.host, self.port))
        channel = grpc.insecure_channel('sqkserver:50051')
        stub = squeak_server_pb2_grpc.SqueakServerStub(channel)
        response = stub.SayHello(squeak_server_pb2.HelloRequest(name='rpc_client'))
        print("Greeter client received: " + response.message)
        logger.info("Greeter client received: " + response.message)
