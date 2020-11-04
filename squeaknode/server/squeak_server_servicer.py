import logging
from concurrent import futures

import grpc
from squeak.core import CSqueak

from proto import squeak_server_pb2, squeak_server_pb2_grpc
from squeaknode.server.util import get_hash

logger = logging.getLogger(__name__)


class SqueakServerServicer(squeak_server_pb2_grpc.SqueakServerServicer):
    """Provides methods that implement functionality of squeak server."""

    def __init__(self, host, port, handler):
        self.host = host
        self.port = port
        self.handler = handler

    def PostSqueak(self, request, context):
        squeak_msg = request.squeak

        squeak_hash = squeak_msg.hash
        squeak = CSqueak.deserialize(squeak_msg.serialized_squeak)
        # Check is squeak deserialized correctly
        if squeak == None:
            context.set_code(grpc.StatusCode.INVALID_ARGUMENT)
            return squeak_server_pb2.PostSqueakReply()

        # Check if squeak hash is correct
        if get_hash(squeak) != squeak_hash:
            context.set_code(grpc.StatusCode.INVALID_ARGUMENT)
            return squeak_server_pb2.PostSqueakReply()

        # Check if squeak is unlocked
        if not squeak.HasDecryptionKey():
            context.set_code(grpc.StatusCode.INVALID_ARGUMENT)
            return squeak_server_pb2.PostSqueakReply()

        # Insert the squeak in database.
        self.handler.handle_posted_squeak(squeak)
        return squeak_server_pb2.PostSqueakReply()

    def GetSqueak(self, request, context):
        squeak_hash = request.hash
        # TODO: check if hash is valid

        squeak = self.handler.handle_get_squeak(squeak_hash)
        if squeak == None:
            context.set_code(grpc.StatusCode.NOT_FOUND)
            context.set_details("Squeak not found.")
            return squeak_server_pb2.GetSqueakReply(
                squeak=None,
            )

        return squeak_server_pb2.GetSqueakReply(
            squeak=squeak_server_pb2.Squeak(
                hash=get_hash(squeak),
                serialized_squeak=squeak.serialize(),
            )
        )

    def LookupSqueaks(self, request, context):
        return self.handler.handle_lookup_squeaks(request)

    def BuySqueak(self, request, context):
        squeak_hash = request.hash
        # TODO: check if hash is valid
        challenge = request.challenge

        buy_response = self.handler.handle_buy_squeak(squeak_hash, challenge)

        if buy_response == None:
            context.set_code(grpc.StatusCode.NOT_FOUND)
            context.set_details("Squeak not found.")
            return squeak_server_pb2.BuySqueakReply(
                offer=None,
            )

        offer_squeak_hash = buy_response.squeak_hash

        return squeak_server_pb2.BuySqueakReply(
            offer=squeak_server_pb2.SqueakBuyOffer(
                squeak_hash=offer_squeak_hash,
                key_cipher=buy_response.key_cipher.cipher_bytes,
                iv=buy_response.iv,
                preimage_hash=buy_response.preimage_hash,
                payment_request=buy_response.payment_request,
                host=buy_response.host,
                port=buy_response.port,
                proof=buy_response.proof,
            ),
        )

    def serve(self):
        server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
        squeak_server_pb2_grpc.add_SqueakServerServicer_to_server(self, server)
        # server.add_insecure_port('0.0.0.0:50052')
        server.add_insecure_port("{}:{}".format(self.host, self.port))
        server.start()
        server.wait_for_termination()
