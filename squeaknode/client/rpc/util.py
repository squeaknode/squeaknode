
from squeak.core import CSqueak

from squeaknode.client.rpc import route_guide_pb2
from squeaknode.client.rpc import route_guide_pb2_grpc


def build_squeak_msg(squeak):
    return route_guide_pb2.Squeak(
        hash=squeak.GetHash(),
        serialized_squeak=squeak.serialize(),
    )


def squeak_from_msg(squeak_msg):
    return CSqueak.deserialize(squeak_msg.serialized_squeak)
