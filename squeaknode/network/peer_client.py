import logging
import time
from contextlib import contextmanager
from typing import List

import grpc
from squeak.core import CSqueak

from proto import squeak_server_pb2
from proto import squeak_server_pb2_grpc
from squeaknode.core.offer import Offer
from squeaknode.network.messages import offer_from_msg
from squeaknode.network.messages import squeak_from_msg
from squeaknode.network.messages import squeak_to_msg


logger = logging.getLogger(__name__)


class PeerClient:
    def __init__(self, host, port, timeout_s):
        self.host = host
        self.port = port
        self.timeout_s = timeout_s
        self.stub = None
        self.start_time_s = None

    @contextmanager
    def open_stub(self):
        host_port_str = "{}:{}".format(self.host, self.port)
        with grpc.insecure_channel(host_port_str) as server_channel:
            self.stub = squeak_server_pb2_grpc.SqueakServerStub(server_channel)
            self.start_time_s = time.time()
            yield self
            self.stub = None
            self.start_time_s = None

    @property
    def ellapsed_time_s(self):
        return time.time() - self.start_time_s

    @property
    def remaining_time_s(self):
        if self.timeout_s is not None:
            return self.timeout_s - self.ellapsed_time_s

    def lookup_squeaks_to_download(self, network: str, addresses: List[str], min_block: int, max_block: int):
        request = squeak_server_pb2.LookupSqueaksToDownloadRequest(
            network=network,
            addresses=addresses,
            min_block=min_block,
            max_block=max_block,
        )
        lookup_response = self.stub.LookupSqueaksToDownload(
            request,
            timeout=self.remaining_time_s,
        )
        return lookup_response

    def lookup_squeaks_to_upload(self, network: str, addresses: List[str]):
        request = squeak_server_pb2.LookupSqueaksToUploadRequest(
            network=network,
            addresses=addresses,
        )
        lookup_response = self.stub.LookupSqueaksToUpload(
            request,
            timeout=self.remaining_time_s,
        )
        return lookup_response

    def upload_squeak(self, squeak: CSqueak) -> None:
        squeak_msg = squeak_to_msg(squeak)
        request = squeak_server_pb2.UploadSqueakRequest(
            squeak=squeak_msg,
        )
        self.stub.UploadSqueak(
            request,
            timeout=self.remaining_time_s,
        )

    def download_squeak(self, squeak_hash: bytes) -> CSqueak:
        request = squeak_server_pb2.DownloadSqueakRequest(
            hash=squeak_hash,
        )
        get_response = self.stub.DownloadSqueak(
            request,
            timeout=self.remaining_time_s,
        )
        return squeak_from_msg(get_response.squeak)

    def download_offer(self, squeak_hash: bytes) -> Offer:
        request = squeak_server_pb2.DownloadOfferRequest(
            hash=squeak_hash,
        )
        download_offer_response = self.stub.DownloadOffer(
            request,
            timeout=self.remaining_time_s,
        )
        return offer_from_msg(download_offer_response.offer)
