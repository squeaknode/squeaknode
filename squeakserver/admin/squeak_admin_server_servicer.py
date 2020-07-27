import sys

import logging
from concurrent import futures

import grpc

from proto import squeak_admin_pb2, squeak_admin_pb2_grpc

from squeakserver.server.util import get_hash, get_replyto

logger = logging.getLogger(__name__)


class SqueakAdminServerServicer(squeak_admin_pb2_grpc.SqueakAdminServicer):
    """Provides methods that implement functionality of squeak admin server."""

    def __init__(self, host, port, handler):
        self.host = host
        self.port = port
        self.handler = handler

    def SayHello(self, request, context):
        return squeak_admin_pb2.HelloReply(message='Hello, %s!' % request.name)

    def LndGetInfo(self, request, context):
        return self.handler.handle_lnd_get_info()

    def LndWalletBalance(self, request, context):
        return self.handler.handle_lnd_wallet_balance()

    def CreateSigningProfile(self, request, context):
        profile_name = request.profile_name
        profile_id = self.handler.handle_create_signing_profile(profile_name)
        return squeak_admin_pb2.CreateSigningProfileReply(profile_id=profile_id,)

    def CreateContactProfile(self, request, context):
        profile_name = request.profile_name
        squeak_address = request.address
        profile_id = self.handler.handle_create_contact_profile(
            profile_name,
            squeak_address,
        )
        return squeak_admin_pb2.CreateContactProfileReply(profile_id=profile_id,)

    def GetSigningProfiles(self, request, context):
        profiles = self.handler.handle_get_signing_profiles()
        profile_msgs = [
            self._squeak_profile_to_message(profile)
            for profile in
            profiles
        ]
        return squeak_admin_pb2.GetSigningProfilesReply(
            squeak_profiles=profile_msgs
        )

    def GetContactProfiles(self, request, context):
        profiles = self.handler.handle_get_contact_profiles()
        profile_msgs = [
            self._squeak_profile_to_message(profile)
            for profile in
            profiles
        ]
        return squeak_admin_pb2.GetContactProfilesReply(
            squeak_profiles=profile_msgs
        )

    def GetSqueakProfile(self, request, context):
        profile_id = request.profile_id
        squeak_profile = self.handler.handle_get_squeak_profile(profile_id)
        squeak_profile_msg = self._squeak_profile_to_message(squeak_profile)
        return squeak_admin_pb2.GetSqueakProfileReply(
            squeak_profile=squeak_profile_msg
        )

    def GetSqueakProfileByAddress(self, request, context):
        address = request.address
        squeak_profile = self.handler.handle_get_squeak_profile_by_address(address)
        squeak_profile_msg = self._squeak_profile_to_message(squeak_profile)
        return squeak_admin_pb2.GetSqueakProfileReply(
            squeak_profile=squeak_profile_msg
        )

    def MakeSqueak(self, request, context):
        profile_id = request.profile_id
        content_str = request.content
        replyto_hash_str = request.replyto
        replyto_hash = bytes.fromhex(replyto_hash_str) if replyto_hash_str else None
        squeak_hash = self.handler.handle_make_squeak(
            profile_id, content_str, replyto_hash
        )
        squeak_hash_str = squeak_hash.hex()
        return squeak_admin_pb2.MakeSqueakReply(squeak_hash=squeak_hash_str,)

    def GetSqueakDisplay(self, request, context):
        squeak_hash_str = request.squeak_hash
        squeak_hash = bytes.fromhex(squeak_hash_str)
        squeak_entry_with_profile = self.handler.handle_get_squeak_display_entry(
            squeak_hash
        )
        display_message = self._squeak_entry_to_message(squeak_entry_with_profile)
        return squeak_admin_pb2.GetSqueakDisplayReply(
            squeak_display_entry=display_message
        )

    def GetFollowedSqueakDisplays(self, request, context):
        squeak_entries_with_profile = self.handler.handle_get_followed_squeak_display_entries()
        squeak_display_msgs = [
            self._squeak_entry_to_message(entry)
            for entry in
            squeak_entries_with_profile
        ]
        return squeak_admin_pb2.GetFollowedSqueakDisplaysReply(
            squeak_display_entries=squeak_display_msgs
        )

    def GetAddressSqueakDisplays(self, request, context):
        address = request.address
        min_block = 0
        max_block = sys.maxsize
        squeak_entries_with_profile = self.handler.handle_get_squeak_display_entries_for_address(
            address,
            min_block,
            max_block,
        )
        squeak_display_msgs = [
            self._squeak_entry_to_message(entry)
            for entry in
            squeak_entries_with_profile
        ]
        return squeak_admin_pb2.GetFollowedSqueakDisplaysReply(
            squeak_display_entries=squeak_display_msgs
        )

    def _squeak_entry_to_message(self, squeak_entry_with_profile):
        if squeak_entry_with_profile is None:
            return None
        squeak_entry = squeak_entry_with_profile.squeak_entry
        squeak = squeak_entry.squeak
        block_header = squeak_entry.block_header
        is_unlocked = squeak.HasDecryptionKey()
        content_str = squeak.GetDecryptedContentStr() if is_unlocked else None
        squeak_profile = squeak_entry_with_profile.squeak_profile
        is_author_known = squeak_profile is not None
        author_name = squeak_profile.profile_name if squeak_profile else None
        author_address = str(squeak.GetAddress())
        is_reply = squeak.is_reply
        reply_to = get_replyto(squeak).hex() if is_reply else None
        return squeak_admin_pb2.SqueakDisplayEntry(
            squeak_hash=get_hash(squeak).hex(),
            is_unlocked=squeak.HasDecryptionKey(),
            content_str=content_str,
            block_height=squeak.nBlockHeight,
            block_time=block_header.nTime,
            is_author_known=is_author_known,
            author_name=author_name,
            author_address=author_address,
            is_reply=is_reply,
            reply_to=reply_to,
        )

    def _squeak_profile_to_message(self, squeak_profile):
        if squeak_profile is None:
            return None
        has_private_key = squeak_profile.private_key is not None
        return squeak_admin_pb2.SqueakProfile(
            profile_id=squeak_profile.profile_id,
            profile_name=squeak_profile.profile_name,
            has_private_key=has_private_key,
            address=squeak_profile.address,
            sharing=squeak_profile.sharing,
            following=squeak_profile.following,
        )

    def serve(self):
        server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
        squeak_admin_pb2_grpc.add_SqueakAdminServicer_to_server(self, server)
        server.add_insecure_port("{}:{}".format(self.host, self.port))
        server.start()
        server.wait_for_termination()
