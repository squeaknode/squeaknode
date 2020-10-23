import os
import logging

from flask import Flask
from flask import request

from google.protobuf import json_format
from google.protobuf import message

from proto import squeak_admin_pb2, squeak_admin_pb2_grpc
from proto import lnd_pb2, lnd_pb2_grpc


logger = logging.getLogger(__name__)


def create_app(handler):
    # create and configure the app
    logger.info("Starting flask app from directory: {}".format(os.getcwd()))
    app = Flask(__name__, static_folder='/app/static/build', static_url_path='/')
    app.config.from_mapping(
        SECRET_KEY='dev',
    )

    def handle_request(request_message, handle_rpc_request):
        data = request.get_data()
        request_message.ParseFromString(data)
        reply = handle_rpc_request(request_message)
        return reply.SerializeToString(reply)

    @app.route('/')
    def index():
        logger.info("Getting index route.")
        logger.info("os.getcwd(): {}".format(os.getcwd()))
        logger.info("os.listdir(os.getcwd()): {}".format(os.listdir(os.getcwd())))
        return app.send_static_file('index.html')

    @app.route('/hello')
    def hello_world():
        logger.info("Getting hello route.")
        return 'Hello, World!'

    @app.route('/lndgetinfo', methods=["POST"])
    def lndgetinfo():
        return handle_request(
            lnd_pb2.GetInfoRequest(),
            handler.handle_lnd_get_info,
        )

    @app.route('/lndwalletbalance', methods=["POST"])
    def lndwalletbalance():
        return handle_request(
            lnd_pb2.WalletBalanceRequest(),
            handler.handle_lnd_wallet_balance,
        )

    @app.route('/lndgettransactions', methods=["POST"])
    def lndgettransactions():
        return handle_request(
            lnd_pb2.GetTransactionsRequest(),
            handler.handle_lnd_get_transactions,
        )

    @app.route('/lndlistpeers', methods=["POST"])
    def lndlistpeers():
        return handle_request(
            lnd_pb2.ListPeersRequest(),
            handler.handle_lnd_list_peers,
        )

    @app.route('/lndlistchannels', methods=["POST"])
    def lndlistchannels():
        return handle_request(
            lnd_pb2.ListChannelsRequest(),
            handler.handle_lnd_list_channels,
        )

    @app.route('/lndpendingchannels', methods=["POST"])
    def lndpendingchannels():
        return handle_request(
            lnd_pb2.PendingChannelsRequest(),
            handler.handle_lnd_pending_channels,
        )

    @app.route('/lndconnectpeer', methods=["POST"])
    def lndconnectpeer():
        return handle_request(
            lnd_pb2.ConnectPeerRequest(),
            handler.handle_lnd_connect_peer,
        )

    @app.route('/lnddisconnectpeer', methods=["POST"])
    def lnddisconnectpeer():
        return handle_request(
            lnd_pb2.DisconnectPeerRequest(),
            handler.handle_lnd_disconnect_peer,
        )

    @app.route('/lndopenchannelsync', methods=["POST"])
    def lndopenchannelsync():
        return handle_request(
            lnd_pb2.OpenChannelRequest(),
            handler.handle_lnd_open_channel_sync,
        )

    @app.route('/lndclosechannel', methods=["POST"])
    def lndclosechannel():
        return handle_request(
            lnd_pb2.CloseChannelRequest(),
            handler.handle_lnd_close_channel,
        )

    @app.route('/getfollowedsqueakdisplays', methods=["POST"])
    def getfollowedsqueakdisplays():
        return handle_request(
            squeak_admin_pb2.GetFollowedSqueakDisplaysRequest(),
            handler.handle_get_followed_squeak_display_entries,
        )

    @app.route('/getsqueakprofile', methods=["POST"])
    def getsqueakprofile():
        return handle_request(
            squeak_admin_pb2.GetSqueakProfileRequest(),
            handler.handle_get_squeak_profile,
        )

    @app.route('/setsqueakprofilefollowing', methods=["POST"])
    def setsqueakprofilefollowing():
        return handle_request(
            squeak_admin_pb2.SetSqueakProfileFollowingRequest(),
            handler.handle_set_squeak_profile_following,
        )

    @app.route('/setsqueakprofilesharing', methods=["POST"])
    def setsqueakprofilesharing():
        return handle_request(
            squeak_admin_pb2.SetSqueakProfileSharingRequest(),
            handler.handle_set_squeak_profile_sharing,
        )

    @app.route('/setsqueakprofilewhitelisted', methods=["POST"])
    def setsqueakprofilewhitelisted():
        return handle_request(
            squeak_admin_pb2.SetSqueakProfileWhitelistedRequest(),
            handler.handle_set_squeak_profile_whitelisted,
        )

    @app.route('/getpeers', methods=["POST"])
    def getpeers():
        return handle_request(
            squeak_admin_pb2.GetPeersRequest(),
            handler.handle_get_squeak_peers,
        )

    @app.route('/payoffer', methods=["POST"])
    def payoffer():
        return handle_request(
            squeak_admin_pb2.PayOfferRequest(),
            handler.handle_pay_offer,
        )

    @app.route('/getbuyoffers', methods=["POST"])
    def getbuyoffers():
        return handle_request(
            squeak_admin_pb2.GetBuyOffersRequest(),
            handler.handle_get_buy_offers,
        )

    @app.route('/getbuyoffer', methods=["POST"])
    def getbuyoffer():
        return handle_request(
            squeak_admin_pb2.GetBuyOfferRequest(),
            handler.handle_get_buy_offer,
        )

    @app.route('/getpeer', methods=["POST"])
    def getpeer():
        return handle_request(
            squeak_admin_pb2.GetPeerRequest(),
            handler.handle_get_squeak_peer,
        )

    @app.route('/setpeerdownloading', methods=["POST"])
    def setpeerdownloading():
        return handle_request(
            squeak_admin_pb2.SetPeerDownloadingRequest(),
            handler.handle_set_squeak_peer_downloading,
        )

    @app.route('/setpeeruploading', methods=["POST"])
    def setpeeruploading():
        return handle_request(
            squeak_admin_pb2.SetPeerUploadingRequest(),
            handler.handle_set_squeak_peer_uploading,
        )

    @app.route('/getsigningprofiles', methods=["POST"])
    def getsigningprofiles():
        return handle_request(
            squeak_admin_pb2.GetSigningProfilesRequest(),
            handler.handle_get_signing_profiles,
        )

    @app.route('/getcontactprofiles', methods=["POST"])
    def getcontactprofiles():
        return handle_request(
            squeak_admin_pb2.GetContactProfilesRequest(),
            handler.handle_get_contact_profiles,
        )

    return app


def run_app(handler):
    app = create_app(handler)
    app.run(
        host="0.0.0.0",
        port=5000,
        debug=False,
    )
