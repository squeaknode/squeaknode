import logging
from concurrent import futures

import grpc

from squeak.core import CSqueak

from squeakserver.admin.rpc import squeak_admin_pb2
from squeakserver.admin.rpc import squeak_admin_pb2_grpc
from squeakserver.server.util import get_hash


logger = logging.getLogger(__name__)


class SqueakAdminServerServicer(squeak_admin_pb2_grpc.SqueakAdminServicer):
    """Provides methods that implement functionality of squeak admin server."""

    def __init__(self, host, port, handler):
        self.host = host
        self.port = port
        self.handler = handler

    def GetBalance(self, request, context):
        total_balance = self.handler.handle_get_balance()
        return squeak_admin_pb2.GetBalanceReply(
            balance=total_balance,
        )

    def CreateSigningProfile(self, request, context):
        profile_name = request.profile_name
        profile_id = self.handler.handle_create_signing_profile(profile_name)
        return squeak_admin_pb2.CreateSigningProfileReply(
            profile_id=profile_id,
        )

    def GetSqueakProfile(self, request, context):
        profile_id = request.profile_id
        squeak_profile = self.handler.handle_get_squeak_profile(profile_id)
        return squeak_admin_pb2.GetSqueakProfileReply(
            squeak_profile=squeak_admin_pb2.SqueakProfile(
                profile_id=squeak_profile.profile_id,
                profile_name=squeak_profile.profile_name,
                private_key=squeak_profile.private_key,
                address=squeak_profile.address,
                sharing=squeak_profile.sharing,
                following=squeak_profile.following,
            )
        )

    def serve(self):
        server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
        squeak_admin_pb2_grpc.add_SqueakAdminServicer_to_server(
            self, server)
        server.add_insecure_port('{}:{}'.format(self.host, self.port))
        server.start()
        server.wait_for_termination()
