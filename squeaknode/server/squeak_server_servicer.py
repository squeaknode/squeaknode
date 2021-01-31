import logging
from concurrent import futures

import grpc

from proto import squeak_server_pb2
from proto import squeak_server_pb2_grpc
from squeaknode.network.messages import offer_to_msg
from squeaknode.network.messages import squeak_from_msg
from squeaknode.network.messages import squeak_to_msg
from squeaknode.server.util import parse_ip_address

logger = logging.getLogger(__name__)


class SqueakServerServicer(squeak_server_pb2_grpc.SqueakServerServicer):
    """Provides methods that implement functionality of squeak server."""

    def __init__(self, host, port, handler, stopped):
        self.host = host
        self.port = port
        self.handler = handler
        self.stopped = stopped

    def UploadSqueak(self, request, context):
        squeak_msg = request.squeak
        squeak = squeak_from_msg(squeak_msg)
        # Handle the uploaded squeak
        self.handler.handle_posted_squeak(squeak)
        return squeak_server_pb2.UploadSqueakReply()

    def DownloadSqueak(self, request: squeak_server_pb2.DownloadSqueakRequest, context):
        squeak_hash = request.hash
        # Basic hash validity check
        if len(squeak_hash) != 32:
            raise Exception("Invalid squeak hash length.")
        squeak = self.handler.handle_get_squeak(squeak_hash)
        if squeak is None:
            raise Exception("Squeak not found.")
        squeak_msg = squeak_to_msg(squeak)
        return squeak_server_pb2.DownloadSqueakReply(
            squeak=squeak_msg,
        )

    def LookupSqueaksToDownload(self, request, context):
        return self.handler.handle_lookup_squeaks_to_download(request)

    def LookupSqueaksToUpload(self, request, context):
        return self.handler.handle_lookup_squeaks_to_upload(request)

    def DownloadOffer(self, request, context):
        squeak_hash = request.hash
        # TODO: check if hash is valid
        client_addr = context.peer()
        ip_addr = parse_ip_address(client_addr)
        offer = self.handler.handle_get_offer(squeak_hash, ip_addr)
        if offer is None:
            raise Exception("Offer not found.")
        logger.info("Sending offer: {}".format(offer))
        offer_msg = offer_to_msg(offer)
        return squeak_server_pb2.DownloadOfferReply(
            offer=offer_msg,
        )

    def serve(self):
        server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
        squeak_server_pb2_grpc.add_SqueakServerServicer_to_server(self, server)
        # server.add_insecure_port('0.0.0.0:50052')
        server.add_insecure_port("{}:{}".format(self.host, self.port))
        logger.info("Starting SqueakServerServicer...")
        server.start()
        # server.wait_for_termination()
        self.stopped.wait()
        server.stop(None)
        logger.info("Stopped SqueakServerServicer.")
