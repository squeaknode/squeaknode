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
        display_message = self._squeak_entry_to_message(squeak_entry_with_profile)
        return squeak_admin_pb2.GetSqueakDisplayReply(
            squeak_display_entry=display_message
        )

    def GetFollowedSqueakDisplays(self, request, context):
        squeak_entries_with_profile = self.handler.handle_get_followed_squeak_display_entries()
        ret = []
        for entry in squeak_entries_with_profile:
            display_message = self._squeak_entry_to_message(entry)
            ret.append(display_message)
        return squeak_admin_pb2.GetFollowedSqueakDisplaysReply(
            squeak_display_entries=ret
        )

    def _squeak_entry_to_message(self, squeak_entry_with_profile):
        squeak_entry = squeak_entry_with_profile.squeak_entry
        squeak = squeak_entry.squeak
        block_header = squeak_entry.block_header
        is_unlocked = squeak.HasDecryptionKey()
        content_str = squeak.GetDecryptedContentStr() if is_unlocked else None
        logger.info("Got block_header: {}".format(block_header))
        return squeak_admin_pb2.SqueakDisplayEntry(
            squeak_hash=get_hash(squeak).hex(),
            is_unlocked=squeak.HasDecryptionKey(),
            content_str=content_str,
            block_height=squeak.nBlockHeight,
            block_time=block_header.nTime,
        )

    def serve(self):
        server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
        squeak_admin_pb2_grpc.add_SqueakAdminServicer_to_server(self, server)
        server.add_insecure_port("{}:{}".format(self.host, self.port))
        server.start()
        server.wait_for_termination()
