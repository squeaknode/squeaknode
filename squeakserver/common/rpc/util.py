
from squeak.core import CSqueak

from squeakserver.common.rpc import squeak_server_pb2
from squeakserver.common.rpc import squeak_server_pb2_grpc


def build_squeak_msg(squeak):
    return squeak_server_pb2.Squeak(
        hash=squeak.GetHash(),
        serialized_squeak=squeak.serialize(),
    )


def squeak_from_msg(squeak_msg):
    return CSqueak.deserialize(squeak_msg.serialized_squeak)
