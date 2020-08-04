import logging

from contextlib import contextmanager

import grpc

from squeakserver.server.util import get_hash

from proto import lnd_pb2 as ln
from proto import (
    squeak_admin_pb2,
    squeak_admin_pb2_grpc,
    squeak_server_pb2,
    squeak_server_pb2_grpc,
)

logger = logging.getLogger(__name__)



class PeerClient:
    def __init__(self, host, port):
        self.host = host
        self.port = port

    @contextmanager
    def get_stub(self):
        host_port_str = "{}:{}".format(self.host, self.port)
        with grpc.insecure_channel(host_port_str) as server_channel:
            yield squeak_server_pb2_grpc.SqueakServerStub(server_channel)

    def lookup_squeaks(self, addresses, min_block, max_block):
        with self.get_stub() as stub:
            lookup_response = stub.LookupSqueaks(
                squeak_server_pb2.LookupSqueaksRequest(
                    addresses=addresses, min_block=0, max_block=99999999,
                )
            )
            return lookup_response.hashes

    def post_squeak(self, squeak):
        squeak_msg = self._build_squeak_msg(squeak)
        with self.get_stub() as stub:
            stub.PostSqueak(
                squeak_server_pb2.PostSqueakRequest(
                    squeak=squeak_msg,
                )
            )

    def _get_hash(self, squeak):
        """ Needs to be reversed because hash is stored as little-endian """
        return squeak.GetHash()[::-1]

    def _build_squeak_msg(self, squeak):
        return squeak_server_pb2.Squeak(
            hash=self._get_hash(squeak),
            serialized_squeak=squeak.serialize(),
        )
