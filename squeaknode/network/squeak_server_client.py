import logging
from contextlib import contextmanager

import grpc
from squeak.core import CheckSqueak, CSqueak

from squeaknode.core.util import get_hash

from proto import squeak_server_pb2, squeak_server_pb2_grpc

logger = logging.getLogger(__name__)


class SqueakServerClient:

    @contextmanager
    def get_stub(self, host, port):
        host_port_str = "{}:{}".format(host, port)
        with grpc.insecure_channel(host_port_str) as server_channel:
            yield squeak_server_pb2_grpc.SqueakServerStub(server_channel)

    def lookup_squeaks(self, stub, addresses, min_block, max_block):
        lookup_response = stub.LookupSqueaks(
            squeak_server_pb2.LookupSqueaksRequest(
                addresses=addresses,
                min_block=min_block,
                max_block=max_block,
            )
        )
        return lookup_response

    def post_squeak(self, stub, squeak):
        squeak_msg = self._build_squeak_msg(squeak)
        stub.PostSqueak(
            squeak_server_pb2.PostSqueakRequest(
                squeak=squeak_msg,
            )
        )

    def get_squeak(self, stub, squeak_hash):
        get_response = stub.GetSqueak(
            squeak_server_pb2.GetSqueakRequest(
                hash=squeak_hash,
            )
        )
        get_response_squeak = self._squeak_from_msg(get_response.squeak)
        CheckSqueak(get_response_squeak, skipDecryptionCheck=True)
        return get_response_squeak

    def buy_squeak(self, stub, squeak_hash):
        buy_response = stub.GetOffer(
            squeak_server_pb2.GetOfferRequest(
                hash=squeak_hash,
            )
        )
        offer_msg = buy_response.offer
        return offer_msg

    def _build_squeak_msg(self, squeak):
        return squeak_server_pb2.Squeak(
            hash=get_hash(squeak),
            serialized_squeak=squeak.serialize(),
        )

    def _squeak_from_msg(self, squeak_msg):
        if not squeak_msg:
            return None
        if not squeak_msg.serialized_squeak:
            return None
        return CSqueak.deserialize(squeak_msg.serialized_squeak)
