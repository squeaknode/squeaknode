import logging
import sys

from proto import squeak_admin_pb2
from squeaknode.admin.messages import connected_peer_to_message
from squeaknode.admin.messages import message_to_peer_address
from squeaknode.admin.messages import offer_entry_to_message
from squeaknode.admin.messages import payment_summary_to_message
from squeaknode.admin.messages import received_payments_to_message
from squeaknode.admin.messages import sent_offer_to_message
from squeaknode.admin.messages import sent_payment_to_message
from squeaknode.admin.messages import squeak_entry_to_detail_message
from squeaknode.admin.messages import squeak_entry_to_message
from squeaknode.admin.messages import squeak_peer_to_message
from squeaknode.admin.messages import squeak_profile_to_message
from squeaknode.admin.profile_image_util import base64_string_to_bytes
from squeaknode.lightning.lnd_lightning_client import LNDLightningClient
from squeaknode.node.squeak_controller import SqueakController

logger = logging.getLogger(__name__)


class SqueakAdminServerHandler(object):
    """Handles admin server commands."""

    def __init__(
        self,
        lightning_client: LNDLightningClient,
        squeak_controller: SqueakController,
    ):
        self.lightning_client = lightning_client
        self.squeak_controller = squeak_controller

    def handle_lnd_get_info(self, request):
        logger.info("Handle lnd get info")
        return self.lightning_client.stub.GetInfo(request)

    def handle_lnd_wallet_balance(self, request):
        logger.info("Handle lnd wallet balance")
        return self.lightning_client.stub.WalletBalance(request)

    def handle_lnd_new_address(self, request):
        logger.info("Handle lnd new address: {}".format(request))
        return self.lightning_client.stub.NewAddress(request)

    def handle_lnd_list_channels(self, request):
        logger.info("Handle lnd list channels")
        return self.lightning_client.stub.ListChannels(request)

    def handle_lnd_pending_channels(self, request):
        logger.info("Handle lnd pending channels")
        return self.lightning_client.stub.PendingChannels(request)

    def handle_lnd_get_transactions(self, request):
        logger.info("Handle lnd get transactions")
        return self.lightning_client.stub.GetTransactions(request)

    def handle_lnd_list_peers(self, request):
        logger.info("Handle list peers")
        return self.lightning_client.stub.ListPeers(request)

    def handle_lnd_connect_peer(self, request):
        logger.info("Handle connect peer: {}".format(request))
        return self.lightning_client.stub.ConnectPeer(request)

    def handle_lnd_disconnect_peer(self, request):
        logger.info("Handle disconnect peer: {}".format(request))
        return self.lightning_client.stub.DisconnectPeer(request)

    def handle_lnd_open_channel_sync(self, request):
        logger.info("Handle open channel: {}".format(request))
        return self.lightning_client.stub.OpenChannelSync(request)

    def handle_lnd_close_channel(self, request):
        logger.info("Handle close channel: {}".format(request))
        return self.lightning_client.stub.CloseChannel(request)

    def handle_lnd_subscribe_channel_events(self, request):
        logger.info("Handle subscribe channel events")
        return self.lightning_client.stub.SubscribeChannelEvents(request)

    def handle_lnd_send_coins(self, request):
        logger.info("Handle send coins.")
        return self.lightning_client.stub.SendCoins(request)

    def handle_create_signing_profile(self, request):
        profile_name = request.profile_name
        logger.info(
            "Handle create signing profile with name: {}".format(profile_name))
        profile_id = self.squeak_controller.create_signing_profile(
            profile_name)
        logger.info("New profile_id: {}".format(profile_id))
        return squeak_admin_pb2.CreateSigningProfileReply(
            profile_id=profile_id,
        )

    def handle_import_signing_profile(self, request):
        profile_name = request.profile_name
        private_key = request.private_key
        logger.info(
            "Handle import signing profile with name: {}".format(profile_name))
        profile_id = self.squeak_controller.import_signing_profile(
            profile_name, private_key)
        logger.info("New profile_id: {}".format(profile_id))
        return squeak_admin_pb2.ImportSigningProfileReply(
            profile_id=profile_id,
        )

    def handle_create_contact_profile(self, request):
        profile_name = request.profile_name
        squeak_address = request.address
        logger.info(
            "Handle create contact profile with name: {}, address: {}".format(
                profile_name,
                squeak_address,
            )
        )
        profile_id = self.squeak_controller.create_contact_profile(
            profile_name, squeak_address
        )
        logger.info("New profile_id: {}".format(profile_id))
        return squeak_admin_pb2.CreateContactProfileReply(
            profile_id=profile_id,
        )

    def handle_get_signing_profiles(self, request):
        logger.info("Handle get signing profiles.")
        profiles = self.squeak_controller.get_signing_profiles()
        logger.info("Got number of signing profiles: {}".format(len(profiles)))
        profile_msgs = [squeak_profile_to_message(
            profile) for profile in profiles]
        return squeak_admin_pb2.GetSigningProfilesReply(squeak_profiles=profile_msgs)

    def handle_get_contact_profiles(self, request):
        logger.info("Handle get contact profiles.")
        profiles = self.squeak_controller.get_contact_profiles()
        logger.info("Got number of contact profiles: {}".format(len(profiles)))
        profile_msgs = [squeak_profile_to_message(
            profile) for profile in profiles]
        return squeak_admin_pb2.GetContactProfilesReply(squeak_profiles=profile_msgs)

    def handle_get_squeak_profile(self, request):
        profile_id = request.profile_id
        logger.info("Handle get squeak profile with id: {}".format(profile_id))
        squeak_profile = self.squeak_controller.get_squeak_profile(profile_id)
        if squeak_profile is None:
            return squeak_admin_pb2.GetSqueakProfileReply(
                squeak_profile=None,
            )
        squeak_profile_msg = squeak_profile_to_message(squeak_profile)
        return squeak_admin_pb2.GetSqueakProfileReply(
            squeak_profile=squeak_profile_msg,
        )

    def handle_get_squeak_profile_by_address(self, request):
        address = request.address
        logger.info(
            "Handle get squeak profile with address: {}".format(address))
        squeak_profile = self.squeak_controller.get_squeak_profile_by_address(
            address)
        if squeak_profile is None:
            return squeak_admin_pb2.GetSqueakProfileByAddressReply(
                squeak_profile=None
            )
        squeak_profile_msg = squeak_profile_to_message(squeak_profile)
        return squeak_admin_pb2.GetSqueakProfileByAddressReply(
            squeak_profile=squeak_profile_msg
        )

    def handle_get_squeak_profile_by_name(self, request):
        name = request.name
        logger.info("Handle get squeak profile with name: {}".format(name))
        squeak_profile = self.squeak_controller.get_squeak_profile_by_name(
            name)
        if squeak_profile is None:
            return squeak_admin_pb2.GetSqueakProfileByNameReply(
                squeak_profile=None
            )
        squeak_profile_msg = squeak_profile_to_message(squeak_profile)
        return squeak_admin_pb2.GetSqueakProfileByNameReply(
            squeak_profile=squeak_profile_msg
        )

    def handle_set_squeak_profile_following(self, request):
        profile_id = request.profile_id
        following = request.following
        logger.info(
            "Handle set squeak profile following with profile id: {}, following: {}".format(
                profile_id,
                following,
            )
        )
        self.squeak_controller.set_squeak_profile_following(
            profile_id, following)
        return squeak_admin_pb2.SetSqueakProfileFollowingReply()

    def handle_rename_squeak_profile(self, request):
        profile_id = request.profile_id
        profile_name = request.profile_name
        logger.info(
            "Handle rename squeak profile with profile id: {}, new name: {}".format(
                profile_id,
                profile_name,
            )
        )
        self.squeak_controller.rename_squeak_profile(profile_id, profile_name)
        return squeak_admin_pb2.RenameSqueakProfileReply()

    def handle_delete_squeak_profile(self, request):
        profile_id = request.profile_id
        logger.info(
            "Handle delete squeak profile with id: {}".format(profile_id))
        self.squeak_controller.delete_squeak_profile(profile_id)
        return squeak_admin_pb2.DeleteSqueakProfileReply()

    def handle_set_squeak_profile_image(self, request):
        profile_id = request.profile_id
        profile_image = request.profile_image
        logger.info(
            "Handle set squeak profile image with profile id: {}".format(
                profile_id,
            )
        )
        profile_image_bytes = base64_string_to_bytes(profile_image)
        self.squeak_controller.set_squeak_profile_image(
            profile_id, profile_image_bytes)
        return squeak_admin_pb2.SetSqueakProfileImageReply()

    def handle_clear_squeak_profile_image(self, request):
        profile_id = request.profile_id
        logger.info(
            "Handle clear squeak profile image with profile id: {}".format(
                profile_id,
            )
        )
        self.squeak_controller.clear_squeak_profile_image(
            profile_id,
        )
        return squeak_admin_pb2.ClearSqueakProfileImageReply()

    def handle_get_squeak_profile_private_key(self, request):
        profile_id = request.profile_id
        logger.info(
            "Handle get squeak profile private key for id: {}".format(profile_id))
        private_key = self.squeak_controller.get_squeak_profile_private_key(
            profile_id)
        return squeak_admin_pb2.GetSqueakProfilePrivateKeyReply(
            private_key=private_key
        )

    def handle_make_squeak(self, request):
        profile_id = request.profile_id
        content_str = request.content
        replyto_hash_str = request.replyto
        replyto_hash = bytes.fromhex(
            replyto_hash_str) if replyto_hash_str else None
        logger.info("Handle make squeak profile with id: {}".format(profile_id))
        inserted_squeak_hash = self.squeak_controller.make_squeak(
            profile_id, content_str, replyto_hash
        )
        return squeak_admin_pb2.MakeSqueakReply(
            squeak_hash=inserted_squeak_hash.hex(),
        )

    def handle_get_squeak_display_entry(self, request):
        squeak_hash_str = request.squeak_hash
        squeak_hash = bytes.fromhex(squeak_hash_str)
        logger.info(
            "Handle get squeak display entry for hash: {}".format(squeak_hash_str))
        squeak_entry_with_profile = (
            self.squeak_controller.get_squeak_entry_with_profile(
                squeak_hash
            )
        )
        if squeak_entry_with_profile is None:
            return squeak_admin_pb2.GetSqueakDisplayReply(
                squeak_display_entry=None
            )
        display_message = squeak_entry_to_message(
            squeak_entry_with_profile)
        return squeak_admin_pb2.GetSqueakDisplayReply(
            squeak_display_entry=display_message
        )

    def handle_get_timeline_squeak_display_entries(self, request):
        logger.info("Handle get timeline squeak display entries.")
        squeak_entries_with_profile = (
            self.squeak_controller.get_timeline_squeak_entries_with_profile()
        )
        logger.info(
            "Got number of timeline squeak entries: {}".format(
                len(squeak_entries_with_profile)
            )
        )
        squeak_display_msgs = [
            squeak_entry_to_message(entry) for entry in squeak_entries_with_profile
        ]
        return squeak_admin_pb2.GetTimelineSqueakDisplaysReply(
            squeak_display_entries=squeak_display_msgs
        )

    def handle_get_squeak_display_entries_for_address(self, request):
        address = request.address
        min_block = 0
        max_block = sys.maxsize
        logger.info(
            "Handle get squeak display entries for address: {}".format(address))
        squeak_entries_with_profile = (
            self.squeak_controller.get_squeak_entries_with_profile_for_address(
                address,
                min_block,
                max_block,
            )
        )
        logger.info(
            "Got number of squeak entries for address: {}".format(
                len(squeak_entries_with_profile)
            )
        )
        squeak_display_msgs = [
            squeak_entry_to_message(entry) for entry in squeak_entries_with_profile
        ]
        return squeak_admin_pb2.GetAddressSqueakDisplaysReply(
            squeak_display_entries=squeak_display_msgs
        )

    def handle_get_ancestor_squeak_display_entries(self, request):
        squeak_hash_str = request.squeak_hash
        squeak_hash = bytes.fromhex(squeak_hash_str)
        logger.info(
            "Handle get ancestor squeak display entries for squeak hash: {}".format(
                squeak_hash_str
            )
        )
        squeak_entries_with_profile = (
            self.squeak_controller.get_ancestor_squeak_entries_with_profile(
                squeak_hash,
            )
        )
        logger.info(
            "Got number of ancestor squeak entries: {}".format(
                len(squeak_entries_with_profile)
            )
        )
        squeak_display_msgs = [
            squeak_entry_to_message(entry) for entry in squeak_entries_with_profile
        ]
        return squeak_admin_pb2.GetAncestorSqueakDisplaysReply(
            squeak_display_entries=squeak_display_msgs
        )

    def handle_get_reply_squeak_display_entries(self, request):
        squeak_hash_str = request.squeak_hash
        squeak_hash = bytes.fromhex(squeak_hash_str)
        logger.info(
            "Handle get reply squeak display entries for squeak hash: {}".format(
                squeak_hash_str
            )
        )
        squeak_entries_with_profile = (
            self.squeak_controller.get_reply_squeak_entries_with_profile(
                squeak_hash,
            )
        )
        logger.info(
            "Got number of reply squeak entries: {}".format(
                len(squeak_entries_with_profile)
            )
        )
        squeak_display_msgs = [
            squeak_entry_to_message(entry) for entry in squeak_entries_with_profile
        ]
        return squeak_admin_pb2.GetReplySqueakDisplaysReply(
            squeak_display_entries=squeak_display_msgs
        )

    def handle_delete_squeak(self, request):
        squeak_hash_str = request.squeak_hash
        squeak_hash = bytes.fromhex(squeak_hash_str)
        logger.info(
            "Handle delete squeak with hash: {}".format(squeak_hash_str))
        self.squeak_controller.delete_squeak(squeak_hash)
        logger.info(
            "Deleted squeak entry with hash: {}".format(squeak_hash_str))
        return squeak_admin_pb2.DeleteSqueakReply()

    def handle_create_peer(self, request):
        peer_name = request.peer_name
        host = request.host
        port = request.port
        logger.info(
            "Handle create peer with name: {}, host: {}, port: {}".format(
                peer_name,
                host,
                port,
            )
        )
        peer_id = self.squeak_controller.create_peer(
            peer_name,
            host,
            port,
        )
        return squeak_admin_pb2.CreatePeerReply(
            peer_id=peer_id,
        )

    def handle_get_squeak_peer(self, request):
        peer_id = request.peer_id
        logger.info("Handle get squeak peer with id: {}".format(peer_id))
        squeak_peer = self.squeak_controller.get_peer(peer_id)
        if squeak_peer is None:
            return squeak_admin_pb2.GetPeerReply(
                squeak_peer=None,
            )
        squeak_peer_msg = squeak_peer_to_message(squeak_peer)
        return squeak_admin_pb2.GetPeerReply(
            squeak_peer=squeak_peer_msg,
        )

    def handle_get_squeak_peers(self, request):
        logger.info("Handle get squeak peers")
        squeak_peers = self.squeak_controller.get_peers()
        squeak_peer_msgs = [
            squeak_peer_to_message(squeak_peer)
            for squeak_peer in squeak_peers
        ]
        return squeak_admin_pb2.GetPeersReply(
            squeak_peers=squeak_peer_msgs,
        )

    def handle_rename_squeak_peer(self, request):
        peer_id = request.peer_id
        peer_name = request.peer_name
        logger.info(
            "Handle rename peer with peer id: {}, new name: {}".format(
                peer_id,
                peer_name,
            )
        )
        self.squeak_controller.rename_peer(peer_id, peer_name)
        return squeak_admin_pb2.RenamePeerReply()

    def handle_set_squeak_peer_autoconnect(self, request):
        peer_id = request.peer_id
        autoconnect = request.autoconnect
        logger.info(
            "Handle set peer autoconnect with peer id: {}, autoconnect: {}".format(
                peer_id,
                autoconnect,
            )
        )
        self.squeak_controller.set_peer_autoconnect(peer_id, autoconnect)
        return squeak_admin_pb2.SetPeerAutoconnectReply()

    def handle_delete_squeak_peer(self, request):
        peer_id = request.peer_id
        logger.info("Handle delete squeak peer with id: {}".format(peer_id))
        self.squeak_controller.delete_peer(peer_id)
        return squeak_admin_pb2.DeletePeerReply()

    def handle_get_buy_offers(self, request):
        squeak_hash_str = request.squeak_hash
        squeak_hash = bytes.fromhex(squeak_hash_str)
        logger.info(
            "Handle get received offers for hash: {}".format(squeak_hash_str))
        offers = self.squeak_controller.get_received_offers(
            squeak_hash)
        offer_msgs = [offer_entry_to_message(offer) for offer in offers]
        return squeak_admin_pb2.GetBuyOffersReply(
            offers=offer_msgs,
        )

    def handle_get_buy_offer(self, request):
        offer_id = request.offer_id
        logger.info("Handle get buy offer for hash: {}".format(offer_id))
        offer = self.squeak_controller.get_received_offer(offer_id)
        if offer is None:
            return squeak_admin_pb2.GetBuyOfferReply(
                offer=None,
            )
        offer_msg = offer_entry_to_message(offer)
        return squeak_admin_pb2.GetBuyOfferReply(
            offer=offer_msg,
        )

    def handle_sync_squeaks(self, request):
        logger.info("Handle sync squeaks")
        # sync_result = self.squeak_controller.sync_squeaks()
        # self.sync_controller.download_timeline()
        # self.sync_controller.upload_timeline()
        self.squeak_controller.sync_timeline()
        return squeak_admin_pb2.SyncSqueaksReply()

    def handle_sync_squeak(self, request):
        squeak_hash_str = request.squeak_hash
        squeak_hash = bytes.fromhex(squeak_hash_str)
        logger.info(
            "Handle download squeak with hash: {}".format(squeak_hash_str))
        # TODO: Add a separate method for download squeak and upload squeak.
        # self.sync_controller.download_single_squeak(squeak_hash)
        # self.sync_controller.upload_single_squeak(squeak_hash)
        self.squeak_controller.download_single_squeak(squeak_hash)
        return squeak_admin_pb2.SyncSqueakReply()

    def handle_download_offers(self, request):
        squeak_hash_str = request.squeak_hash
        squeak_hash = bytes.fromhex(squeak_hash_str)
        logger.info(
            "Handle download offer for hash: {}".format(squeak_hash_str))
        # sync_result = self.squeak_controller.sync_squeaks()
        # self.sync_controller.download_timeline()
        # self.sync_controller.upload_timeline()
        self.squeak_controller.download_offers(squeak_hash)
        return squeak_admin_pb2.DownloadOffersReply()

    def handle_download_replies(self, request):
        squeak_hash_str = request.squeak_hash
        squeak_hash = bytes.fromhex(squeak_hash_str)
        logger.info(
            "Handle download replies for hash: {}".format(squeak_hash_str))
        self.squeak_controller.download_replies(squeak_hash)
        return squeak_admin_pb2.DownloadRepliesReply()

    def handle_pay_offer(self, request):
        offer_id = request.offer_id
        logger.info("Handle pay offer for offer id: {}".format(offer_id))
        sent_payment_id = self.squeak_controller.pay_offer(offer_id)
        return squeak_admin_pb2.PayOfferReply(
            sent_payment_id=sent_payment_id,
        )

    def handle_get_sent_payments(self, request):
        logger.info("Handle get sent payments")
        sent_payments = self.squeak_controller.get_sent_payments()
        sent_payment_msgs = [
            sent_payment_to_message(sent_payment)
            for sent_payment in sent_payments
        ]
        return squeak_admin_pb2.GetSentPaymentsReply(
            sent_payments=sent_payment_msgs,
        )

    def handle_get_sent_payment(self, request):
        sent_payment_id = request.sent_payment_id
        logger.info(
            "Handle get sent payment with id: {}".format(sent_payment_id))
        sent_payment = self.squeak_controller.get_sent_payment(sent_payment_id)
        if sent_payment is None:
            return squeak_admin_pb2.GetSentPaymentReply(
                sent_payment=None,
            )
        sent_payment_msg = sent_payment_to_message(sent_payment)
        return squeak_admin_pb2.GetSentPaymentReply(
            sent_payment=sent_payment_msg,
        )

    def handle_get_squeak_details(self, request: squeak_admin_pb2.GetSqueakDetailsRequest):
        squeak_hash_str = request.squeak_hash
        squeak_hash = bytes.fromhex(squeak_hash_str)
        logger.info(
            "Handle get squeak details for hash: {}".format(squeak_hash_str))
        squeak_entry_with_profile = (
            self.squeak_controller.get_squeak_entry_with_profile(
                squeak_hash
            )
        )
        if squeak_entry_with_profile is None:
            return squeak_admin_pb2.GetSqueakDetailsReply(
                squeak_detail_entry=None
            )
        detail_message = squeak_entry_to_detail_message(
            squeak_entry_with_profile)
        return squeak_admin_pb2.GetSqueakDetailsReply(
            squeak_detail_entry=detail_message
        )

    def handle_get_sent_offers(self, request):
        logger.info("Handle get sent offers")
        sent_offers = self.squeak_controller.get_sent_offers()
        sent_offer_msgs = [
            sent_offer_to_message(sent_offer) for sent_offer in sent_offers
        ]
        return squeak_admin_pb2.GetSentOffersReply(
            sent_offers=sent_offer_msgs,
        )

    def handle_get_received_payments(self, request):
        logger.info("Handle get received payments")
        received_payments = self.squeak_controller.get_received_payments()
        received_payment_msgs = [
            received_payments_to_message(received_payment)
            for received_payment in received_payments
        ]
        return squeak_admin_pb2.GetReceivedPaymentsReply(
            received_payments=received_payment_msgs,
        )

    def handle_subscribe_received_payments(self, request, stopped):
        payment_index = request.payment_index
        logger.info(
            "Handle subscribe received payments with index: {}".format(
                payment_index)
        )
        received_payments_stream = self.squeak_controller.subscribe_received_payments(
            payment_index,
            stopped,
        )
        for received_payment in received_payments_stream:
            received_payment_msg = received_payments_to_message(
                received_payment)
            yield received_payment_msg

    def handle_get_network(self, request):
        logger.info("Handle get network")
        network = self.squeak_controller.get_network()
        return squeak_admin_pb2.GetNetworkReply(
            network=network,
        )

    def handle_get_payment_summary(self, request):
        logger.info("Handle get payment summary")
        received_payment_summary = self.squeak_controller.get_received_payment_summary()
        sent_payment_summary = self.squeak_controller.get_sent_payment_summary()
        payment_summary_msg = payment_summary_to_message(
            received_payment_summary,
            sent_payment_summary,
        )
        return squeak_admin_pb2.GetPaymentSummaryReply(
            payment_summary=payment_summary_msg,
        )

    def handle_reprocess_received_payments(self, request):
        logger.info("Handle reprocess received payments")
        self.squeak_controller.reprocess_received_payments()
        return squeak_admin_pb2.ReprocessReceivedPaymentsReply()

    def handle_like_squeak(self, request: squeak_admin_pb2.LikeSqueakRequest):
        squeak_hash_str = request.squeak_hash
        squeak_hash = bytes.fromhex(squeak_hash_str)
        logger.info(
            "Handle like squeak with hash: {}".format(squeak_hash_str))
        self.squeak_controller.like_squeak(
            squeak_hash
        )
        return squeak_admin_pb2.LikeSqueakReply()

    def handle_unlike_squeak(self, request: squeak_admin_pb2.UnlikeSqueakRequest):
        squeak_hash_str = request.squeak_hash
        squeak_hash = bytes.fromhex(squeak_hash_str)
        logger.info(
            "Handle unlike squeak with hash: {}".format(squeak_hash_str))
        self.squeak_controller.unlike_squeak(
            squeak_hash
        )
        return squeak_admin_pb2.UnlikeSqueakReply()

    def handle_get_liked_squeak_display_entries(self, request):
        logger.info("Handle get liked squeak display entries.")
        squeak_entries_with_profile = (
            self.squeak_controller.get_liked_squeak_entries_with_profile()
        )
        squeak_display_msgs = [
            squeak_entry_to_message(entry) for entry in squeak_entries_with_profile
        ]
        return squeak_admin_pb2.GetTimelineSqueakDisplaysReply(
            squeak_display_entries=squeak_display_msgs
        )

    def handle_connect_peer(self, request):
        peer_address = message_to_peer_address(request.peer_address)
        logger.info(
            "Handle connect peer with peer address: {}".format(peer_address))
        self.squeak_controller.connect_peer(peer_address)
        return squeak_admin_pb2.ConnectPeerReply()

    def handle_get_connected_peers(self, request):
        logger.info("Handle get connected peers.")
        connected_peers = self.squeak_controller.get_connected_peers()
        logger.info("Connected peers: {}".format(
            connected_peers,
        ))
        connected_peers_display_msgs = [
            connected_peer_to_message(peer) for peer in connected_peers
        ]
        return squeak_admin_pb2.GetConnectedPeersReply(
            connected_peers=connected_peers_display_msgs
        )

    def handle_get_connected_peer(self, request):
        host = request.host
        port = request.port
        logger.info("Handle get connected peer host: {}, port: {}".format(
            host, port
        ))
        connected_peer = self.squeak_controller.get_connected_peer(host, port)
        logger.info("Connected peer: {}".format(
            connected_peer,
        ))
        if connected_peer is None:
            return squeak_admin_pb2.GetConnectedPeerReply(
                connected_peer=None
            )
        connected_peers_display_msg = connected_peer_to_message(connected_peer)
        return squeak_admin_pb2.GetConnectedPeerReply(
            connected_peer=connected_peers_display_msg
        )

    def handle_disconnect_peer(self, request):
        peer_address = message_to_peer_address(request.peer_address)
        logger.info(
            "Handle connect peer with peer address: {}".format(peer_address))
        self.squeak_controller.disconnect_peer(peer_address)
        return squeak_admin_pb2.DisconnectPeerReply()

    def handle_subscribe_connected_peers(self, request, stopped):
        logger.info("Handle subscribe connected peers")
        connected_peers_stream = self.squeak_controller.subscribe_connected_peers(
            stopped,
        )
        for connected_peers in connected_peers_stream:
            connected_peers_display_msgs = [
                connected_peer_to_message(peer) for peer in connected_peers
            ]
            yield squeak_admin_pb2.GetConnectedPeersReply(
                connected_peers=connected_peers_display_msgs
            )
