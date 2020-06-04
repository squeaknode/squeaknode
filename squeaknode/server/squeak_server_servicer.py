# Copyright 2015 gRPC authors.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
"""The Python implementation of the gRPC route guide server."""
import math
import time
from concurrent import futures

import grpc

from squeaknode.common.rpc import squeak_server_pb2
from squeaknode.common.rpc import squeak_server_pb2_grpc
from squeaknode.common.rpc.util import squeak_from_msg


class SqueakServerServicer(squeak_server_pb2_grpc.SqueakServerServicer):
    """Provides methods that implement functionality of squeak server."""

    def __init__(self, host, port, handler):
        self.host = host
        self.port = port
        self.handler = handler

    def SayHello(self, request, context):
        return squeak_server_pb2.HelloReply(message='Hello, %s!' % request.name)

    # def WalletBalance(self, request, context):
    #     response = self.node.get_wallet_balance()
    #     return route_guide_pb2.WalletBalanceResponse(
    #         total_balance=response.total_balance,
    #         confirmed_balance=response.confirmed_balance,
    #         unconfirmed_balance=response.unconfirmed_balance,
    #     )

    def PostSqueak(self, request, context):
        squeak_msg = request.squeak
        squeak = squeak_from_msg(squeak_msg)
        squeak_hash = self.handler.handle_posted_squeak(squeak)
        return squeak_server_pb2.PostSqueakReply(
            hash=squeak_hash,
        )

    def serve(self):
        print('Calling serve...', flush=True)
        server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
        squeak_server_pb2_grpc.add_SqueakServerServicer_to_server(
            self, server)
        # server.add_insecure_port('0.0.0.0:50052')
        server.add_insecure_port('{}:{}'.format(self.host, self.port))
        print("Starting SqueakServerServicer rpc server...", flush=True)
        server.start()
        print("Started SqueakServerServicer rpc server...", flush=True)
        server.wait_for_termination()
