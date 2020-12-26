import logging
import sys

from proto import squeak_admin_pb2
from squeaknode.admin.util import (
    offer_entry_to_message,
    received_payments_to_message,
    sent_offer_to_message,
    sent_payment_with_peer_to_message,
    squeak_entry_to_detail_message,
    squeak_entry_to_message,
    squeak_peer_to_message,
    squeak_profile_to_message,
    sync_result_to_message,
)
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

    def handle_create_signing_profile(self, request):
        profile_name = request.profile_name
        logger.info("Handle create signing profile with name: {}".format(profile_name))
        profile_id = self.squeak_controller.create_signing_profile(profile_name)
        logger.info("New profile_id: {}".format(profile_id))
        return squeak_admin_pb2.CreateSigningProfileReply(
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
        profile_msgs = [squeak_profile_to_message(profile) for profile in profiles]
        return squeak_admin_pb2.GetSigningProfilesReply(squeak_profiles=profile_msgs)

    def handle_get_contact_profiles(self, request):
        logger.info("Handle get contact profiles.")
        profiles = self.squeak_controller.get_contact_profiles()
        logger.info("Got number of contact profiles: {}".format(len(profiles)))
        profile_msgs = [squeak_profile_to_message(profile) for profile in profiles]
        return squeak_admin_pb2.GetContactProfilesReply(squeak_profiles=profile_msgs)

    def handle_get_squeak_profile(self, request):
        profile_id = request.profile_id
        logger.info("Handle get squeak profile with id: {}".format(profile_id))
        squeak_profile = self.squeak_controller.get_squeak_profile(profile_id)
        if squeak_profile is None:
            return None
        squeak_profile_msg = squeak_profile_to_message(squeak_profile)
        return squeak_admin_pb2.GetSqueakProfileReply(
            squeak_profile=squeak_profile_msg,
        )

    def handle_get_squeak_profile_by_address(self, request):
        address = request.address
        logger.info("Handle get squeak profile with address: {}".format(address))
        squeak_profile = self.squeak_controller.get_squeak_profile_by_address(address)
        squeak_profile_msg = squeak_profile_to_message(squeak_profile)
        return squeak_admin_pb2.GetSqueakProfileByAddressReply(
            squeak_profile=squeak_profile_msg
        )

    def handle_get_squeak_profile_by_name(self, request):
        name = request.name
        logger.info("Handle get squeak profile with name: {}".format(name))
        squeak_profile = self.squeak_controller.get_squeak_profile_by_name(name)
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
        self.squeak_controller.set_squeak_profile_following(profile_id, following)
        return squeak_admin_pb2.SetSqueakProfileFollowingReply()

    def handle_set_squeak_profile_sharing(self, request):
        profile_id = request.profile_id
        sharing = request.sharing
        logger.info(
            "Handle set squeak profile sharing with profile id: {}, sharing: {}".format(
                profile_id,
                sharing,
            )
        )
        self.squeak_controller.set_squeak_profile_sharing(profile_id, sharing)
        return squeak_admin_pb2.SetSqueakProfileSharingReply()

    def handle_delete_squeak_profile(self, request):
        profile_id = request.profile_id
        logger.info("Handle delete squeak profile with id: {}".format(profile_id))
        self.squeak_controller.delete_squeak_profile(profile_id)
        return squeak_admin_pb2.DeleteSqueakProfileReply()

    def handle_make_squeak(self, request):
        profile_id = request.profile_id
        content_str = request.content
        replyto_hash_str = request.replyto
        replyto_hash = bytes.fromhex(replyto_hash_str) if replyto_hash_str else None
        logger.info("Handle make squeak profile with id: {}".format(profile_id))
        inserted_squeak_hash = self.squeak_controller.make_squeak(
            profile_id, content_str, replyto_hash
        )
        return squeak_admin_pb2.MakeSqueakReply(
            squeak_hash=inserted_squeak_hash,
        )

    def handle_get_squeak_display_entry(self, request):
        squeak_hash = request.squeak_hash
        logger.info("Handle get squeak display entry for hash: {}".format(squeak_hash))
        squeak_entry_with_profile = (
            self.squeak_controller.get_squeak_entry_with_profile(squeak_hash)
        )
        logger.info("Squeak display entry: {}".format(squeak_entry_with_profile))
        display_message = squeak_entry_to_message(squeak_entry_with_profile)
        logger.info(
            "Returning squeak display entry message: {}".format(display_message)
        )
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
        logger.info("Handle get squeak display entries for address: {}".format(address))
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
        squeak_hash = request.squeak_hash
        logger.info(
            "Handle get ancestor squeak display entries for squeak hash: {}".format(
                squeak_hash
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

    def handle_delete_squeak(self, request):
        squeak_hash = request.squeak_hash
        logger.info("Handle delete squeak with hash: {}".format(squeak_hash))
        self.squeak_controller.delete_squeak(squeak_hash)
        logger.info("Deleted squeak entry with hash: {}".format(squeak_hash))
        return squeak_admin_pb2.DeleteSqueakReply()

    def handle_create_peer(self, request):
        peer_name = request.peer_name if request.peer_name else None
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
            return None
        squeak_peer_msg = squeak_peer_to_message(squeak_peer)
        return squeak_admin_pb2.GetPeerReply(
            squeak_peer=squeak_peer_msg,
        )

    def handle_get_squeak_peers(self, request):
        logger.info("Handle get squeak peers")
        squeak_peers = self.squeak_controller.get_peers()
        squeak_peer_msgs = [
            squeak_peer_to_message(squeak_peer) for squeak_peer in squeak_peers
        ]
        return squeak_admin_pb2.GetPeersReply(
            squeak_peers=squeak_peer_msgs,
        )

    def handle_set_squeak_peer_downloading(self, request):
        peer_id = request.peer_id
        downloading = request.downloading
        logger.info(
            "Handle set peer downloading with peer id: {}, downloading: {}".format(
                peer_id,
                downloading,
            )
        )
        self.squeak_controller.set_peer_downloading(peer_id, downloading)
        return squeak_admin_pb2.SetPeerDownloadingReply()

    def handle_set_squeak_peer_uploading(self, request):
        peer_id = request.peer_id
        uploading = request.uploading
        logger.info(
            "Handle set peer uploading with peer id: {}, uploading: {}".format(
                peer_id,
                uploading,
            )
        )
        self.squeak_controller.set_peer_uploading(peer_id, uploading)
        return squeak_admin_pb2.SetPeerUploadingReply()

    def handle_delete_squeak_peer(self, request):
        peer_id = request.peer_id
        logger.info("Handle delete squeak peer with id: {}".format(peer_id))
        self.squeak_controller.delete_peer(peer_id)
        return squeak_admin_pb2.DeletePeerReply()

    def handle_get_buy_offers(self, request):
        squeak_hash = request.squeak_hash
        logger.info("Handle get buy offers for hash: {}".format(squeak_hash))
        offers = self.squeak_controller.get_buy_offers_with_peer(squeak_hash)
        offer_msgs = [offer_entry_to_message(offer) for offer in offers]
        return squeak_admin_pb2.GetBuyOffersReply(
            offers=offer_msgs,
        )

    def handle_get_buy_offer(self, request):
        offer_id = request.offer_id
        logger.info("Handle get buy offer for hash: {}".format(offer_id))
        offer = self.squeak_controller.get_buy_offer_with_peer(offer_id)
        offer_msg = offer_entry_to_message(offer)
        return squeak_admin_pb2.GetBuyOfferReply(
            offer=offer_msg,
        )

    def handle_sync_squeaks(self, request):
        logger.info("Handle sync squeaks")
        sync_result = self.squeak_controller.sync_squeaks()
        sync_result_msg = sync_result_to_message(sync_result)
        return squeak_admin_pb2.SyncSqueaksReply(
            sync_result=sync_result_msg,
        )

    def handle_sync_squeak(self, request):
        squeak_hash = request.squeak_hash
        logger.info("Handle download squeak with hash: {}".format(squeak_hash))
        sync_result = self.squeak_controller.sync_squeak(squeak_hash)
        sync_result_msg = sync_result_to_message(sync_result)
        return squeak_admin_pb2.SyncSqueakReply(
            sync_result=sync_result_msg,
        )

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
            sent_payment_with_peer_to_message(sent_payment)
            for sent_payment in sent_payments
        ]
        return squeak_admin_pb2.GetSentPaymentsReply(
            sent_payments=sent_payment_msgs,
        )

    def handle_get_sent_payment(self, request):
        sent_payment_id = request.sent_payment_id
        logger.info("Handle get sent payment with id: {}".format(sent_payment_id))
        sent_payment = self.squeak_controller.get_sent_payment(sent_payment_id)
        sent_payment_msg = sent_payment_with_peer_to_message(sent_payment)
        return squeak_admin_pb2.GetSentPaymentReply(
            sent_payment=sent_payment_msg,
        )

    def handle_get_squeak_details(self, request):
        squeak_hash = request.squeak_hash
        logger.info("Handle get squeak details for hash: {}".format(squeak_hash))
        squeak_entry_with_profile = (
            self.squeak_controller.get_squeak_entry_with_profile(squeak_hash)
        )
        detail_message = squeak_entry_to_detail_message(squeak_entry_with_profile)
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

    def handle_subscribe_received_payments(self, request):
        payment_index = request.payment_index
        logger.info(
            "Handle subscribe received payments with index: {}".format(payment_index)
        )
        received_payments_stream = self.squeak_controller.subscribe_received_payments(
            payment_index
        )
        for received_payment in received_payments_stream:
            received_payment_msg = received_payments_to_message(received_payment)
            yield received_payment_msg
