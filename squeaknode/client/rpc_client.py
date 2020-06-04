import logging

import grpc

from squeaknode.common.rpc import squeak_server_pb2
from squeaknode.common.rpc import squeak_server_pb2_grpc
from squeaknode.common.rpc.util import build_squeak_msg
from squeaknode.common.rpc.util import squeak_from_msg

from squeak.core.signing import CSigningKey
from squeak.core.signing import CSqueakAddress

from squeaknode.client.squeak_store import SqueakStore
from squeaknode.common.blockchain_client import BlockchainClient
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
        logger.info('Trying to connect to {}:{}'.format(self.host, self.port))
        channel = grpc.insecure_channel('{}:{}'.format(self.host, self.port))
        # channel = grpc.insecure_channel('sqkserver:50052')
        stub = squeak_server_pb2_grpc.SqueakServerStub(channel)
        response = stub.SayHello(squeak_server_pb2.HelloRequest(name='rpc_client'))
        logger.info("Greeter client received: " + response.message)

        logger.info("Building squeak msg with squeak: " + str(squeak))
        squeak_msg = build_squeak_msg(squeak)
        logger.info("Building squeak msg with squeak_msg: " + str(squeak_msg))
        response2 = stub.PostSqueak(squeak_server_pb2.PostSqueakRequest(squeak=squeak_msg))
        logger.info("Post squeak client received: " + str(response2.hash))

    def download_squeak(self, squeak_hash):
        logger.info("Download the squeak here.")

        # Make the rpc request to the server.
        channel = grpc.insecure_channel('{}:{}'.format(self.host, self.port))
        # channel = grpc.insecure_channel('sqkserver:50052')
        stub = squeak_server_pb2_grpc.SqueakServerStub(channel)
        response = stub.GetSqueak(squeak_server_pb2.GetSqueakRequest(hash=squeak_hash))
        logger.info("Get squeak client received: " + str(response.squeak))
        return squeak_from_msg(response.squeak)
