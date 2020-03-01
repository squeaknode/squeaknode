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
from squeaknode.client.rpc import route_guide_resources


def get_feature(feature_db, point):
    """Returns Feature at given location or None."""
    for feature in feature_db:
        if feature.location == point:
            return feature
    return None


def get_distance(start, end):
    """Distance between two points."""
    coord_factor = 10000000.0
    lat_1 = start.latitude / coord_factor
    lat_2 = end.latitude / coord_factor
    lon_1 = start.longitude / coord_factor
    lon_2 = end.longitude / coord_factor
    lat_rad_1 = math.radians(lat_1)
    lat_rad_2 = math.radians(lat_2)
    delta_lat_rad = math.radians(lat_2 - lat_1)
    delta_lon_rad = math.radians(lon_2 - lon_1)

    # Formula is based on http://mathforum.org/library/drmath/view/51879.html
    a = (pow(math.sin(delta_lat_rad / 2), 2) +
         (math.cos(lat_rad_1) * math.cos(lat_rad_2) * pow(
             math.sin(delta_lon_rad / 2), 2)))
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
    R = 6371000
    # metres
    return R * c


class RouteGuideServicer(route_guide_pb2_grpc.RouteGuideServicer):
    """Provides methods that implement functionality of route guide server."""

    def __init__(self, node):
        self.db = route_guide_resources.read_route_guide_database()
        self.node = node

    def GetFeature(self, request, context):
        feature = get_feature(self.db, request)
        if feature is None:
            return route_guide_pb2.Feature(name="", location=request)
        else:
            return feature

    def ListFeatures(self, request, context):
        left = min(request.lo.longitude, request.hi.longitude)
        right = max(request.lo.longitude, request.hi.longitude)
        top = max(request.lo.latitude, request.hi.latitude)
        bottom = min(request.lo.latitude, request.hi.latitude)
        for feature in self.db:
            if (feature.location.longitude >= left and
                    feature.location.longitude <= right and
                    feature.location.latitude >= bottom and
                    feature.location.latitude <= top):
                yield feature

    def RecordRoute(self, request_iterator, context):
        point_count = 0
        feature_count = 0
        distance = 0.0
        prev_point = None

        start_time = time.time()
        for point in request_iterator:
            point_count += 1
            if get_feature(self.db, point):
                feature_count += 1
            if prev_point:
                distance += get_distance(prev_point, point)
            prev_point = point

        elapsed_time = time.time() - start_time
        return route_guide_pb2.RouteSummary(
            point_count=point_count,
            feature_count=feature_count,
            distance=int(distance),
            elapsed_time=int(elapsed_time))

    def RouteChat(self, request_iterator, context):
        prev_notes = []
        for new_note in request_iterator:
            for prev_note in prev_notes:
                if prev_note.location == new_note.location:
                    yield prev_note
            prev_notes.append(new_note)

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
        squeak_msg = route_guide_pb2.Squeak(
            hash=squeak.GetHash(),
            address=str(squeak.GetAddress()),
            content=squeak.GetDecryptedContentStr(),
            block_height=squeak.nBlockHeight,
            timestamp=squeak.nTime,
        )
        return route_guide_pb2.MakeSqueakResponse(
            squeak=squeak_msg,
        )

    def GenerateSigningKey(self, request, context):
        address = self.node.generate_signing_key()
        return route_guide_pb2.GenerateSigningKeyResponse(
            address=str(address),
        )

    def serve(self):
        server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
        route_guide_pb2_grpc.add_RouteGuideServicer_to_server(
            self, server)
        server.add_insecure_port('0.0.0.0:50051')
        server.start()
        server.wait_for_termination()
