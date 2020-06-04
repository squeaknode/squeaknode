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

from squeaknode.client.rpc import route_guide_pb2
from squeaknode.client.rpc import route_guide_pb2_grpc
from squeaknode.client.rpc.util import build_squeak_msg


class RouteGuideServicer(route_guide_pb2_grpc.RouteGuideServicer):
    """Provides methods that implement functionality of route guide server."""

    def __init__(self, node):
        self.node = node

    def WalletBalance(self, request, context):
        response = self.node.get_wallet_balance()
        return route_guide_pb2.WalletBalanceResponse(
            total_balance=response.total_balance,
            confirmed_balance=response.confirmed_balance,
            unconfirmed_balance=response.unconfirmed_balance,
        )

    def ConnectHost(self, request, context):
        host = request.host
        self.node.connect_host(host)
        return route_guide_pb2.ConnectHostResponse()

    def DisconnectPeer(self, request, context):
        addr = request.addr
        host = addr.host
        port = addr.port
        address = (host, port)
        self.node.disconnect_peer(address)
        return route_guide_pb2.DisconnectPeerResponse()

    def ListPeers(self, request, context):
        peers = self.node.get_peers()
        peer_msgs = [
            route_guide_pb2.Peer(
                addr=route_guide_pb2.Addr(
                    host=peer.address[0],
                    port=peer.address[1],
                ),
            )
            for peer in peers
        ]
        return route_guide_pb2.ListPeersResponse(
            peers=peer_msgs,
        )

    def MakeSqueak(self, request, context):
        content = request.content
        squeak = self.node.make_squeak(content)
        squeak_msg = self.build_squeak_msg(squeak)
        return route_guide_pb2.MakeSqueakResponse(
            squeak=squeak_msg,
        )

    def GetSqueak(self, request, context):
        squeak_hash = request.hash
        squeak = self.node.get_squeak(squeak_hash)
        squeak_msg = self.build_squeak_msg(squeak)
        return route_guide_pb2.GetSqueakResponse(
            squeak=squeak_msg,
        )

    def GenerateSigningKey(self, request, context):
        address = self.node.generate_signing_key()
        return route_guide_pb2.GenerateSigningKeyResponse(
            address=str(address),
        )

    def build_squeak_msg(self, squeak):
        if squeak == None:
            return None
        return build_squeak_msg(squeak)


    def serve(self):
        server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
        route_guide_pb2_grpc.add_RouteGuideServicer_to_server(
            self, server)
        server.add_insecure_port('0.0.0.0:50051')
        server.start()
        server.wait_for_termination()
