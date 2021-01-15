import logging
from concurrent import futures

import grpc
from squeak.core import CSqueak

from proto import squeak_server_pb2
from proto import squeak_server_pb2_grpc
from squeaknode.core.util import get_hash
from squeaknode.server.util import parse_ip_address

logger = logging.getLogger(__name__)


class SqueakServerServicer(squeak_server_pb2_grpc.SqueakServerServicer):
    """Provides methods that implement functionality of squeak server."""

    def __init__(self, host, port, handler):
        self.host = host
        self.port = port
        self.handler = handler

    def UploadSqueak(self, request, context):
        squeak_msg = request.squeak

        squeak_hash = squeak_msg.hash
        squeak = CSqueak.deserialize(squeak_msg.serialized_squeak)
        # Check is squeak deserialized correctly
        if squeak is None:
            context.set_code(grpc.StatusCode.INVALID_ARGUMENT)
            return squeak_server_pb2.UploadSqueakReply()

        # Check if squeak hash is correct
        if get_hash(squeak) != squeak_hash:
            context.set_code(grpc.StatusCode.INVALID_ARGUMENT)
            return squeak_server_pb2.UploadSqueakReply()

        # Check if squeak is unlocked
        if not squeak.HasDecryptionKey():
            context.set_code(grpc.StatusCode.INVALID_ARGUMENT)
            return squeak_server_pb2.UploadSqueakReply()

        # Insert the squeak in database.
        self.handler.handle_posted_squeak(squeak)
        return squeak_server_pb2.UploadSqueakReply()

    def DownloadSqueak(self, request: squeak_server_pb2.DownloadSqueakRequest, context):
        squeak_hash = request.hash
        # TODO: check if hash is valid

        squeak = self.handler.handle_get_squeak(squeak_hash)
        if squeak is None:
            context.set_code(grpc.StatusCode.NOT_FOUND)
            context.set_details("Squeak not found.")
            return squeak_server_pb2.DownloadSqueakReply(
                squeak=None,
            )

        return squeak_server_pb2.DownloadSqueakReply(
            squeak=squeak_server_pb2.Squeak(
                hash=get_hash(squeak),
                serialized_squeak=squeak.serialize(),
            )
        )

    def LookupSqueaksToDownload(self, request, context):
        return self.handler.handle_lookup_squeaks_to_download(request)

    def LookupSqueaksToUpload(self, request, context):
        return self.handler.handle_lookup_squeaks_to_upload(request)

    def GetOffer(self, request, context):
        squeak_hash = request.hash
        # TODO: check if hash is valid
        client_addr = context.peer()
        ip_addr = parse_ip_address(client_addr)

        buy_response = self.handler.handle_get_offer(squeak_hash, ip_addr)

        if buy_response is None:
            context.set_code(grpc.StatusCode.NOT_FOUND)
            context.set_details("Offer not found.")
            return squeak_server_pb2.GetOfferReply(
                offer=None,
            )

        logger.info("Sending buy offer: {}".format(buy_response))

        return squeak_server_pb2.GetOfferReply(
            offer=squeak_server_pb2.Offer(
                squeak_hash=buy_response.squeak_hash,
                nonce=buy_response.nonce,
                payment_request=buy_response.payment_request,
                host=buy_response.host,
                port=buy_response.port,
            ),
        )

    def serve(self):
        server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
        squeak_server_pb2_grpc.add_SqueakServerServicer_to_server(self, server)
        # server.add_insecure_port('0.0.0.0:50052')
        server.add_insecure_port("{}:{}".format(self.host, self.port))
        server.start()
        server.wait_for_termination()
