import logging
from concurrent import futures

import grpc

from proto import squeak_admin_pb2, squeak_admin_pb2_grpc

from squeakserver.server.util import get_hash

logger = logging.getLogger(__name__)


class SqueakAdminServerServicer(squeak_admin_pb2_grpc.SqueakAdminServicer):
    """Provides methods that implement functionality of squeak admin server."""

    def __init__(self, host, port, handler):
        self.host = host
        self.port = port
        self.handler = handler

    def GetBalance(self, request, context):
        wallet_balance_response = self.handler.handle_get_balance()
        return squeak_admin_pb2.GetBalanceReply(
            wallet_balance_response=wallet_balance_response,
        )

    def CreateSigningProfile(self, request, context):
        profile_name = request.profile_name
        profile_id = self.handler.handle_create_signing_profile(profile_name)
        return squeak_admin_pb2.CreateSigningProfileReply(profile_id=profile_id,)

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

    def MakeSqueak(self, request, context):
        profile_id = request.profile_id
        content_str = request.content
        replyto_hash = request.replyto
        squeak_hash = self.handler.handle_make_squeak(
            profile_id, content_str, replyto_hash
        )
        return squeak_admin_pb2.MakeSqueakReply(hash=squeak_hash,)

    def GetSqueakDisplay(self, request, context):
        squeak_hash = request.hash
        squeak_entry_with_profile = self.handler.handle_get_squeak_display_entry(
            squeak_hash
        )
        squeak_entry = squeak_entry_with_profile.squeak_entry
        squeak = squeak_entry.squeak
        block_header = squeak_entry.block_header
        logger.info("Got block_header: {}".format(block_header))
        return squeak_admin_pb2.GetSqueakDisplayReply(
            squeak_display_entry=squeak_admin_pb2.SqueakDisplayEntry(
                squeak_hash=get_hash(squeak).hex(),
                is_unlocked=True,
                content_str=squeak.GetDecryptedContentStr(),
                block_height=squeak.nBlockHeight,
                block_time=block_header.nTime,
            )
        )

    def GetFollowedSqueakDisplays(self, request, context):
        squeak_entries_with_profile = self.handler.handle_get_followed_squeak_display_entries()
        ret = []
        for entry in squeak_entries_with_profile:
            squeak_entry = entry.squeak_entry
            squeak = squeak_entry.squeak
            block_header = squeak_entry.block_header
            squeak_display_entry=squeak_admin_pb2.SqueakDisplayEntry(
                squeak_hash=get_hash(squeak).hex(),
                is_unlocked=True,
                content_str=squeak.GetDecryptedContentStr(),
                block_height=squeak.nBlockHeight,
                block_time=block_header.nTime,
            )
            ret.append(squeak_display_entry)
        return squeak_admin_pb2.GetFollowedSqueakDisplaysReply(
            squeak_display_entries=ret
        )

    def serve(self):
        server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
        squeak_admin_pb2_grpc.add_SqueakAdminServicer_to_server(self, server)
        server.add_insecure_port("{}:{}".format(self.host, self.port))
        server.start()
        server.wait_for_termination()
