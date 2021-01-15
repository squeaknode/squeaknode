import logging
from contextlib import contextmanager
from typing import List

import grpc
from squeak.core import CheckSqueak
from squeak.core import CSqueak

from proto import squeak_server_pb2
from proto import squeak_server_pb2_grpc
from squeaknode.core.util import get_hash

logger = logging.getLogger(__name__)


class PeerClient:
    def __init__(self, host, port):
        self.host = host
        self.port = port
        self.stub = None

    @contextmanager
    def open_stub(self):
        host_port_str = "{}:{}".format(self.host, self.port)
        with grpc.insecure_channel(host_port_str) as server_channel:
            self.stub = squeak_server_pb2_grpc.SqueakServerStub(server_channel)
            yield self
            self.stub = None

    def lookup_squeaks(self, addresses: List[str], min_block: int, max_block: int):
        lookup_response = self.stub.LookupSqueaks(
            squeak_server_pb2.LookupSqueaksRequest(
                addresses=addresses,
                min_block=min_block,
                max_block=max_block,
            )
        )
        return lookup_response

    def lookup_squeaks_to_download(self, addresses: List[str], min_block: int, max_block: int):
        lookup_response = self.stub.LookupSqueaksToDownload(
            squeak_server_pb2.LookupSqueaksToDownloadRequest(
                addresses=addresses,
                min_block=min_block,
                max_block=max_block,
            )
        )
        return lookup_response

    def lookup_squeaks_to_upload(self, addresses: List[str]):
        lookup_response = self.stub.LookupSqueaksToUpload(
            squeak_server_pb2.LookupSqueaksToUploadRequest(
                addresses=addresses,
            )
        )
        return lookup_response

    def post_squeak(self, squeak: CSqueak):
        squeak_msg = self._build_squeak_msg(squeak)
        self.stub.PostSqueak(
            squeak_server_pb2.PostSqueakRequest(
                squeak=squeak_msg,
            )
        )

    def get_squeak(self, squeak_hash: bytes):
        get_response = self.stub.GetSqueak(
            squeak_server_pb2.GetSqueakRequest(
                hash=squeak_hash,
            )
        )
        get_response_squeak = self._squeak_from_msg(get_response.squeak)
        CheckSqueak(get_response_squeak, skipDecryptionCheck=True)
        return get_response_squeak

    def get_offer(self, squeak_hash: bytes):
        get_offer_response = self.stub.GetOffer(
            squeak_server_pb2.GetOfferRequest(
                hash=squeak_hash,
            )
        )
        offer_msg = get_offer_response.offer
        return offer_msg

    def _build_squeak_msg(self, squeak: CSqueak):
        return squeak_server_pb2.Squeak(
            hash=get_hash(squeak),
            serialized_squeak=squeak.serialize(),
        )

    def _squeak_from_msg(self, squeak_msg: squeak_server_pb2.Squeak):
        if not squeak_msg:
            return None
        if not squeak_msg.serialized_squeak:
            return None
        return CSqueak.deserialize(squeak_msg.serialized_squeak)
