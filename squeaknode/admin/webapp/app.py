# MIT License
#
# Copyright (c) 2020 Jonathan Zernik
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.
import logging
import os
import threading
from functools import wraps

from flask import flash
from flask import Flask
from flask import redirect
from flask import render_template
from flask import request
from flask import url_for
from flask_cors import CORS
from flask_login import current_user
from flask_login import login_required
from flask_login import login_user
from flask_login import LoginManager
from flask_login import logout_user
from werkzeug.serving import make_server

from proto import lnd_pb2
from proto import squeak_admin_pb2
from squeaknode.admin.webapp.forms import LoginForm
from squeaknode.admin.webapp.squeak_admin_web_user import User

logger = logging.getLogger(__name__)


def create_app(handler, username, password):
    # create and configure the app
    logger.debug("Starting flask app from directory: {}".format(os.getcwd()))
    app = Flask(
        __name__,
        static_url_path="/",
        static_folder="static/build",
    )
    app.config.from_mapping(
        SECRET_KEY="dev",
    )
    login = LoginManager(app)
    valid_user = User(
        username,
        password,
    )
    logger.debug("Starting flask with app.root_path: {}".format(app.root_path))
    logger.debug("Files in root path: {}".format(os.listdir(app.root_path)))

    @login.user_loader
    def load_user(id):
        return valid_user.get_user_by_username(id)

    @login.unauthorized_handler
    def unauthorized_callback():
        return redirect("/login")

    def handle_request(request_message, handle_rpc_request):
        data = request.get_data()
        request_message.ParseFromString(data)
        try:
            reply = handle_rpc_request(request_message)
            return reply.SerializeToString()
        except Exception as e:
            logger.error("Error in handle admin web request.", exc_info=True)
            return str(e), 500

    def protobuf_serialized(request_message):
        def decorator(func):
            @wraps(func)
            def wrapper(*args, **kwargs):
                data = request.get_data()
                request_message.ParseFromString(data)
                try:
                    reply = func(request_message)
                    return reply.SerializeToString()
                except Exception as e:
                    logger.error(
                        "Error in handle admin web request.", exc_info=True)
                    return str(e), 500
            return wrapper
        return decorator

    @app.route("/login", methods=["GET", "POST"])
    def login():
        logger.info("Trying to login")
        if current_user.is_authenticated:
            return redirect(url_for("index"))
        default_username = request.args.get('user')
        form = LoginForm(username=default_username)
        if form.validate_on_submit():
            user = valid_user.get_user_by_username(form.username.data)
            if user is None or not user.check_password(form.password.data):
                flash("Invalid username or password")
                return redirect(url_for("login"))
            login_user(user, remember=form.remember_me.data)
            return redirect(url_for("index"))
        return render_template("login.html", title="Sign In", form=form)

    @app.route("/logout")
    def logout():
        logout_user()
        return redirect(url_for("index"))

    @app.route("/")
    @login_required
    def index():
        logger.info("Getting index route.")
        return app.send_static_file("index.html")

    @app.route("/user")
    @login_required
    def user():
        logger.info("Getting user.")
        return current_user.username

    @app.route("/hello")
    @login_required
    def hello_world():
        logger.info("Getting hello route.")
        return "Hello, World!"

    @app.route("/lndgetinfo", methods=["POST"])
    @login_required
    def lndgetinfo():
        return handle_request(
            lnd_pb2.GetInfoRequest(),
            handler.handle_lnd_get_info,
        )

    @app.route("/lndwalletbalance", methods=["POST"])
    @login_required
    def lndwalletbalance():
        return handle_request(
            lnd_pb2.WalletBalanceRequest(),
            handler.handle_lnd_wallet_balance,
        )

    @app.route("/lndgettransactions", methods=["POST"])
    @login_required
    def lndgettransactions():
        return handle_request(
            lnd_pb2.GetTransactionsRequest(),
            handler.handle_lnd_get_transactions,
        )

    @app.route("/lndlistpeers", methods=["POST"])
    @login_required
    def lndlistpeers():
        return handle_request(
            lnd_pb2.ListPeersRequest(),
            handler.handle_lnd_list_peers,
        )

    @app.route("/lndlistchannels", methods=["POST"])
    @login_required
    def lndlistchannels():
        return handle_request(
            lnd_pb2.ListChannelsRequest(),
            handler.handle_lnd_list_channels,
        )

    @app.route("/lndpendingchannels", methods=["POST"])
    @login_required
    def lndpendingchannels():
        return handle_request(
            lnd_pb2.PendingChannelsRequest(),
            handler.handle_lnd_pending_channels,
        )

    @app.route("/lndconnectpeer", methods=["POST"])
    @login_required
    def lndconnectpeer():
        return handle_request(
            lnd_pb2.ConnectPeerRequest(),
            handler.handle_lnd_connect_peer,
        )

    @app.route("/lnddisconnectpeer", methods=["POST"])
    @login_required
    def lnddisconnectpeer():
        return handle_request(
            lnd_pb2.DisconnectPeerRequest(),
            handler.handle_lnd_disconnect_peer,
        )

    @app.route("/lndopenchannelsync", methods=["POST"])
    @login_required
    def lndopenchannelsync():
        return handle_request(
            lnd_pb2.OpenChannelRequest(),
            handler.handle_lnd_open_channel_sync,
        )

    @app.route("/lndclosechannel", methods=["POST"])
    @login_required
    def lndclosechannel():
        return handle_request(
            lnd_pb2.CloseChannelRequest(),
            handler.handle_lnd_close_channel,
        )

    @app.route("/lndnewaddress", methods=["POST"])
    @login_required
    def lndnewaddress():
        return handle_request(
            lnd_pb2.NewAddressRequest(),
            handler.handle_lnd_new_address,
        )

    @app.route("/lndsendcoins", methods=["POST"])
    @login_required
    def lndsendcoins():
        return handle_request(
            lnd_pb2.SendCoinsRequest(),
            handler.handle_lnd_send_coins,
        )

    @app.route("/gettimelinesqueakdisplays", methods=["POST"])
    @login_required
    @protobuf_serialized(squeak_admin_pb2.GetTimelineSqueakDisplaysRequest())
    def gettimelinesqueakdisplays(msg):
        # return handle_request(
        #     squeak_admin_pb2.GetTimelineSqueakDisplaysRequest(),
        #     handler.handle_get_timeline_squeak_display_entries,
        # )
        return handler.handle_get_timeline_squeak_display_entries(msg)

    @app.route("/getsqueakprofile", methods=["POST"])
    @login_required
    @protobuf_serialized(squeak_admin_pb2.GetSqueakProfileRequest())
    def getsqueakprofile(msg):
        # return handle_request(
        #     squeak_admin_pb2.GetSqueakProfileRequest(),
        #     handler.handle_get_squeak_profile,
        # )
        return handler.handle_get_squeak_profile(msg)

    @app.route("/setsqueakprofilefollowing", methods=["POST"])
    @login_required
    @protobuf_serialized(squeak_admin_pb2.SetSqueakProfileFollowingRequest())
    def setsqueakprofilefollowing(msg):
        # return handle_request(
        #     squeak_admin_pb2.SetSqueakProfileFollowingRequest(),
        #     handler.handle_set_squeak_profile_following,
        # )
        return handler.handle_set_squeak_profile_following(msg)

    @app.route("/setsqueakprofileusecustomprice", methods=["POST"])
    @login_required
    @protobuf_serialized(squeak_admin_pb2.SetSqueakProfileUseCustomPriceRequest())
    def setsqueakprofileusecustomprice(msg):
        # return handle_request(
        #     squeak_admin_pb2.SetSqueakProfileUseCustomPriceRequest(),
        #     handler.handle_set_squeak_profile_use_custom_price,
        # )
        return handler.handle_set_squeak_profile_use_custom_price(msg)

    @app.route("/setsqueakprofilecustomprice", methods=["POST"])
    @login_required
    @protobuf_serialized(squeak_admin_pb2.SetSqueakProfileUseCustomPriceRequest())
    def setsqueakprofilecustomprice(msg):
        # return handle_request(
        #     squeak_admin_pb2.SetSqueakProfileCustomPriceRequest(),
        #     handler.handle_set_squeak_profile_custom_price,
        # )
        return handler.handle_set_squeak_profile_custom_price(msg)

    @app.route("/renamesqueakprofile", methods=["POST"])
    @login_required
    @protobuf_serialized(squeak_admin_pb2.RenameSqueakProfileRequest())
    def renamesqueakprofile(msg):
        # return handle_request(
        #     squeak_admin_pb2.RenameSqueakProfileRequest(),
        #     handler.handle_rename_squeak_profile,
        # )
        return handler.handle_rename_squeak_profile(msg)

    @app.route("/setsqueakprofileimage", methods=["POST"])
    @login_required
    @protobuf_serialized(squeak_admin_pb2.SetSqueakProfileImageRequest())
    def setsqueakprofileimage(msg):
        # return handle_request(
        #     squeak_admin_pb2.SetSqueakProfileImageRequest(),
        #     handler.handle_set_squeak_profile_image,
        # )
        return handler.handle_set_squeak_profile_image(msg)

    @app.route("/clearsqueakprofileimage", methods=["POST"])
    @login_required
    @protobuf_serialized(squeak_admin_pb2.ClearSqueakProfileImageRequest())
    def clearsqueakprofileimage(msg):
        # return handle_request(
        #     squeak_admin_pb2.ClearSqueakProfileImageRequest(),
        #     handler.handle_clear_squeak_profile_image,
        # )
        return handler.handle_clear_squeak_profile_image(msg)

    @app.route("/getpeers", methods=["POST"])
    @login_required
    @protobuf_serialized(squeak_admin_pb2.GetPeersRequest())
    def getpeers(msg):
        # return handle_request(
        #     squeak_admin_pb2.GetPeersRequest(),
        #     handler.handle_get_squeak_peers,
        # )
        return handler.handle_get_squeak_peers(msg)

    @app.route("/payoffer", methods=["POST"])
    @login_required
    @protobuf_serialized(squeak_admin_pb2.PayOfferRequest())
    def payoffer(msg):
        # return handle_request(
        #     squeak_admin_pb2.PayOfferRequest(),
        #     handler.handle_pay_offer,
        # )
        return handler.handle_pay_offer(msg)

    @app.route("/getbuyoffers", methods=["POST"])
    @login_required
    @protobuf_serialized(squeak_admin_pb2.GetBuyOffersRequest())
    def getbuyoffers(msg):
        # return handle_request(
        #     squeak_admin_pb2.GetBuyOffersRequest(),
        #     handler.handle_get_buy_offers,
        # )
        return handler.handle_get_buy_offers(msg)

    @app.route("/getbuyoffer", methods=["POST"])
    @login_required
    @protobuf_serialized(squeak_admin_pb2.GetBuyOfferRequest())
    def getbuyoffer(msg):
        # return handle_request(
        #     squeak_admin_pb2.GetBuyOfferRequest(),
        #     handler.handle_get_buy_offer,
        # )
        return handler.handle_get_buy_offer(msg)

    @app.route("/getpeer", methods=["POST"])
    @login_required
    @protobuf_serialized(squeak_admin_pb2.GetPeerRequest())
    def getpeer(msg):
        # return handle_request(
        #     squeak_admin_pb2.GetPeerRequest(),
        #     handler.handle_get_squeak_peer,
        # )
        return handler.handle_get_squeak_peer(msg)

    @app.route("/getpeerbyaddress", methods=["POST"])
    @login_required
    @protobuf_serialized(squeak_admin_pb2.GetPeerByAddressRequest())
    def getpeerbyaddress(msg):
        # return handle_request(
        #     squeak_admin_pb2.GetPeerByAddressRequest(),
        #     handler.handle_get_squeak_peer_by_address,
        # )
        return handler.handle_get_squeak_peer_by_address(msg)

    @app.route("/setpeerautoconnect", methods=["POST"])
    @login_required
    @protobuf_serialized(squeak_admin_pb2.SetPeerAutoconnectRequest())
    def setpeerautoconnect(msg):
        # return handle_request(
        #     squeak_admin_pb2.SetPeerAutoconnectRequest(),
        #     handler.handle_set_squeak_peer_autoconnect,
        # )
        return handler.handle_set_squeak_peer_autoconnect(msg)

    @app.route("/renamepeer", methods=["POST"])
    @login_required
    @protobuf_serialized(squeak_admin_pb2.RenamePeerRequest())
    def renamepeer(msg):
        # return handle_request(
        #     squeak_admin_pb2.RenamePeerRequest(),
        #     handler.handle_rename_squeak_peer,
        # )
        return handler.handle_rename_squeak_peer(msg)

    @app.route("/getprofiles", methods=["POST"])
    @login_required
    @protobuf_serialized(squeak_admin_pb2.GetProfilesRequest())
    def getprofiles(msg):
        # return handle_request(
        #     squeak_admin_pb2.GetProfilesRequest(),
        #     handler.handle_get_profiles,
        # )
        return handler.handle_get_profiles(msg)

    @app.route("/getsigningprofiles", methods=["POST"])
    @login_required
    @protobuf_serialized(squeak_admin_pb2.GetSigningProfilesRequest())
    def getsigningprofiles(msg):
        # return handle_request(
        #     squeak_admin_pb2.GetSigningProfilesRequest(),
        #     handler.handle_get_signing_profiles,
        # )
        return handler.handle_get_signing_profiles(msg)

    @app.route("/getcontactprofiles", methods=["POST"])
    @login_required
    @protobuf_serialized(squeak_admin_pb2.GetContactProfilesRequest())
    def getcontactprofiles(msg):
        # return handle_request(
        #     squeak_admin_pb2.GetContactProfilesRequest(),
        #     handler.handle_get_contact_profiles,
        # )
        return handler.handle_get_contact_profiles(msg)

    @app.route("/makesqueakrequest", methods=["POST"])
    @login_required
    @protobuf_serialized(squeak_admin_pb2.MakeSqueakRequest())
    def makesqueakrequest(msg):
        # return handle_request(
        #     squeak_admin_pb2.MakeSqueakRequest(),
        #     handler.handle_make_squeak,
        # )
        return handler.handle_make_squeak(msg)

    @app.route("/getsqueakdisplay", methods=["POST"])
    @login_required
    @protobuf_serialized(squeak_admin_pb2.GetSqueakDisplayRequest())
    def getsqueakdisplay(msg):
        # return handle_request(
        #     squeak_admin_pb2.GetSqueakDisplayRequest(),
        #     handler.handle_get_squeak_display_entry,
        # )
        return handler.handle_get_squeak_display_entry(msg)

    @app.route("/getancestorsqueakdisplays", methods=["POST"])
    @login_required
    @protobuf_serialized(squeak_admin_pb2.GetAncestorSqueakDisplaysRequest())
    def getancestorsqueakdisplays(msg):
        # return handle_request(
        #     squeak_admin_pb2.GetAncestorSqueakDisplaysRequest(),
        #     handler.handle_get_ancestor_squeak_display_entries,
        # )
        return handler.handle_get_ancestor_squeak_display_entries(msg)

    @app.route("/getreplysqueakdisplays", methods=["POST"])
    @login_required
    @protobuf_serialized(squeak_admin_pb2.GetReplySqueakDisplaysRequest())
    def getreplysqueakdisplays(msg):
        # return handle_request(
        #     squeak_admin_pb2.GetReplySqueakDisplaysRequest(),
        #     handler.handle_get_reply_squeak_display_entries,
        # )
        return handler.handle_get_reply_squeak_display_entries(msg)

    @app.route("/getsqueakprofilebyaddress", methods=["POST"])
    @login_required
    @protobuf_serialized(squeak_admin_pb2.GetSqueakProfileByAddressRequest())
    def getsqueakprofilebyaddress(msg):
        # return handle_request(
        #     squeak_admin_pb2.GetSqueakProfileByAddressRequest(),
        #     handler.handle_get_squeak_profile_by_address,
        # )
        return handler.handle_get_squeak_profile_by_address(msg)

    @app.route("/getaddresssqueakdisplays", methods=["POST"])
    @login_required
    @protobuf_serialized(squeak_admin_pb2.GetAddressSqueakDisplaysRequest())
    def getaddresssqueakdisplays(msg):
        # return handle_request(
        #     squeak_admin_pb2.GetAddressSqueakDisplaysRequest(),
        #     handler.handle_get_squeak_display_entries_for_address,
        # )
        return handler.handle_get_squeak_display_entries_for_address(msg)

    @app.route("/getsearchsqueakdisplays", methods=["POST"])
    @login_required
    @protobuf_serialized(squeak_admin_pb2.GetSearchSqueakDisplaysRequest())
    def getsearchsqueakdisplays(msg):
        # return handle_request(
        #     squeak_admin_pb2.GetSearchSqueakDisplaysRequest(),
        #     handler.handle_get_squeak_display_entries_for_text_search,
        # )
        return handler.handle_get_squeak_display_entries_for_text_search(msg)

    @app.route("/createcontactprofile", methods=["POST"])
    @login_required
    @protobuf_serialized(squeak_admin_pb2.CreateContactProfileRequest())
    def createcontactprofile(msg):
        # return handle_request(
        #     squeak_admin_pb2.CreateContactProfileRequest(),
        #     handler.handle_create_contact_profile,
        # )
        return handler.handle_create_contact_profile(msg)

    @app.route("/createsigningprofile", methods=["POST"])
    @login_required
    @protobuf_serialized(squeak_admin_pb2.CreateSigningProfileRequest())
    def createsigningprofile(msg):
        # return handle_request(
        #     squeak_admin_pb2.CreateSigningProfileRequest(),
        #     handler.handle_create_signing_profile,
        # )
        return handler.handle_create_signing_profile(msg)

    @app.route("/importsigningprofile", methods=["POST"])
    @login_required
    @protobuf_serialized(squeak_admin_pb2.ImportSigningProfileRequest())
    def importsigningprofile(msg):
        # return handle_request(
        #     squeak_admin_pb2.ImportSigningProfileRequest(),
        #     handler.handle_import_signing_profile,
        # )
        return handler.handle_import_signing_profile(msg)

    @app.route("/createpeer", methods=["POST"])
    @login_required
    @protobuf_serialized(squeak_admin_pb2.CreatePeerRequest())
    def createpeer(msg):
        # return handle_request(
        #     squeak_admin_pb2.CreatePeerRequest(),
        #     handler.handle_create_peer,
        # )
        return handler.handle_create_peer(msg)

    @app.route("/deletepeer", methods=["POST"])
    @login_required
    @protobuf_serialized(squeak_admin_pb2.DeletePeerRequest())
    def deletepeer(msg):
        # return handle_request(
        #     squeak_admin_pb2.DeletePeerRequest(),
        #     handler.handle_delete_squeak_peer,
        # )
        return handler.handle_delete_squeak_peer(msg)

    @app.route("/deleteprofile", methods=["POST"])
    @login_required
    @protobuf_serialized(squeak_admin_pb2.DeleteSqueakProfileRequest())
    def deleteprofile(msg):
        # return handle_request(
        #     squeak_admin_pb2.DeleteSqueakProfileRequest(),
        #     handler.handle_delete_squeak_profile,
        # )
        return handler.handle_delete_squeak_profile(msg)

    @app.route("/deletesqueak", methods=["POST"])
    @login_required
    @protobuf_serialized(squeak_admin_pb2.DeleteSqueakRequest())
    def deletesqueak(msg):
        # return handle_request(
        #     squeak_admin_pb2.DeleteSqueakRequest(),
        #     handler.handle_delete_squeak,
        # )
        return handler.handle_delete_squeak(msg)

    @app.route("/downloadsqueak", methods=["POST"])
    @login_required
    @protobuf_serialized(squeak_admin_pb2.DownloadSqueakRequest())
    def downloadsqueak(msg):
        # return handle_request(
        #     squeak_admin_pb2.DownloadSqueakRequest(),
        #     handler.handle_download_squeak,
        # )
        return handler.handle_download_squeak(msg)

    @app.route("/downloadoffers", methods=["POST"])
    @login_required
    @protobuf_serialized(squeak_admin_pb2.DownloadOffersRequest())
    def downloadoffers(msg):
        # return handle_request(
        #     squeak_admin_pb2.DownloadOffersRequest(),
        #     handler.handle_download_offers,
        # )
        return handler.handle_download_offers(msg)

    @app.route("/downloadreplies", methods=["POST"])
    @login_required
    @protobuf_serialized(squeak_admin_pb2.DownloadRepliesRequest())
    def downloadreplies(msg):
        # return handle_request(
        #     squeak_admin_pb2.DownloadRepliesRequest(),
        #     handler.handle_download_replies,
        # )
        return handler.handle_download_replies(msg)

    @app.route("/downloadaddresssqueaks", methods=["POST"])
    @login_required
    @protobuf_serialized(squeak_admin_pb2.DownloadAddressSqueaksRequest())
    def downloadaddresssqueaks(msg):
        # return handle_request(
        #     squeak_admin_pb2.DownloadAddressSqueaksRequest(),
        #     handler.handle_download_address_squeaks,
        # )
        return handler.handle_download_address_squeaks(msg)

    @app.route("/getsqueakdetails", methods=["POST"])
    @login_required
    @protobuf_serialized(squeak_admin_pb2.GetSqueakDetailsRequest())
    def getsqueakdetails(msg):
        # return handle_request(
        #     squeak_admin_pb2.GetSqueakDetailsRequest(),
        #     handler.handle_get_squeak_details,
        # )
        return handler.handle_get_squeak_details(msg)

    @app.route("/getsentpayments", methods=["POST"])
    @login_required
    @protobuf_serialized(squeak_admin_pb2.GetSentPaymentsRequest())
    def getsentpayments(msg):
        # return handle_request(
        #     squeak_admin_pb2.GetSentPaymentsRequest(),
        #     handler.handle_get_sent_payments,
        # )
        return handler.handle_get_sent_payments(msg)

    @app.route("/getsentoffers", methods=["POST"])
    @login_required
    @protobuf_serialized(squeak_admin_pb2.GetSentOffersRequest())
    def getsentoffers(msg):
        # return handle_request(
        #     squeak_admin_pb2.GetSentOffersRequest(),
        #     handler.handle_get_sent_offers,
        # )
        return handler.handle_get_sent_offers(msg)

    @app.route("/getreceivedpayments", methods=["POST"])
    @login_required
    @protobuf_serialized(squeak_admin_pb2.GetReceivedPaymentsRequest())
    def getreceivedpayments(msg):
        # return handle_request(
        #     squeak_admin_pb2.GetReceivedPaymentsRequest(),
        #     handler.handle_get_received_payments,
        # )
        return handler.handle_get_received_payments(msg)

    @app.route("/getnetwork", methods=["POST"])
    @login_required
    @protobuf_serialized(squeak_admin_pb2.GetNetworkRequest())
    def getnetwork(msg):
        # return handle_request(
        #     squeak_admin_pb2.GetNetworkRequest(),
        #     handler.handle_get_network,
        # )
        return handler.handle_get_network(msg)

    @app.route("/getsqueakprofileprivatekey", methods=["POST"])
    @login_required
    @protobuf_serialized(squeak_admin_pb2.GetSqueakProfilePrivateKeyRequest())
    def getsqueakprofileprivatekey(msg):
        # return handle_request(
        #     squeak_admin_pb2.GetSqueakProfilePrivateKeyRequest(),
        #     handler.handle_get_squeak_profile_private_key,
        # )
        return handler.handle_get_squeak_profile_private_key(msg)

    @app.route("/getpaymentsummary", methods=["POST"])
    @login_required
    @protobuf_serialized(squeak_admin_pb2.GetPaymentSummaryRequest())
    def getpaymentsummary(msg):
        # return handle_request(
        #     squeak_admin_pb2.GetPaymentSummaryRequest(),
        #     handler.handle_get_payment_summary,
        # )
        return handler.handle_get_payment_summary(msg)

    @app.route("/reprocessreceivedpayments", methods=["POST"])
    @login_required
    @protobuf_serialized(squeak_admin_pb2.ReprocessReceivedPaymentsRequest())
    def reprocessreceivedpayments(msg):
        # return handle_request(
        #     squeak_admin_pb2.ReprocessReceivedPaymentsRequest(),
        #     handler.handle_reprocess_received_payments,
        # )
        return handler.handle_reprocess_received_payments(msg)

    @app.route("/likesqueak", methods=["POST"])
    @login_required
    @protobuf_serialized(squeak_admin_pb2.LikeSqueakRequest())
    def likesqueak(msg):
        # return handle_request(
        #     squeak_admin_pb2.LikeSqueakRequest(),
        #     handler.handle_like_squeak,
        # )
        return handler.handle_like_squeak(msg)

    @app.route("/unlikesqueak", methods=["POST"])
    @login_required
    @protobuf_serialized(squeak_admin_pb2.UnlikeSqueakRequest())
    def unlikesqueak(msg):
        # return handle_request(
        #     squeak_admin_pb2.UnlikeSqueakRequest(),
        #     handler.handle_unlike_squeak,
        # )
        return handler.handle_unlike_squeak(msg)

    @app.route("/getlikedsqueakdisplays", methods=["POST"])
    @login_required
    @protobuf_serialized(squeak_admin_pb2.GetLikedSqueakDisplaysRequest())
    def getlikedsqueakdisplays(msg):
        # return handle_request(
        #     squeak_admin_pb2.GetLikedSqueakDisplaysRequest(),
        #     handler.handle_get_liked_squeak_display_entries,
        # )
        return handler.handle_get_liked_squeak_display_entries(msg)

    @app.route("/getconnectedpeers", methods=["POST"])
    @login_required
    @protobuf_serialized(squeak_admin_pb2.GetConnectedPeersRequest())
    def getconnectedpeers(msg):
        # return handle_request(
        #     squeak_admin_pb2.GetConnectedPeersRequest(),
        #     handler.handle_get_connected_peers,
        # )
        return handler.handle_get_connected_peers(msg)

    @app.route("/getconnectedpeer", methods=["POST"])
    @login_required
    @protobuf_serialized(squeak_admin_pb2.GetConnectedPeerRequest())
    def getconnectedpeer(msg):
        # return handle_request(
        #     squeak_admin_pb2.GetConnectedPeerRequest(),
        #     handler.handle_get_connected_peer,
        # )
        return handler.handle_get_connected_peer(msg)

    @app.route("/connectpeer", methods=["POST"])
    @login_required
    @protobuf_serialized(squeak_admin_pb2.ConnectPeerRequest())
    def connectpeer(msg):
        # return handle_request(
        #     squeak_admin_pb2.ConnectPeerRequest(),
        #     handler.handle_connect_peer,
        # )
        return handler.handle_connect_peer(msg)

    @app.route("/disconnectpeer", methods=["POST"])
    @login_required
    @protobuf_serialized(squeak_admin_pb2.DisconnectPeerRequest())
    def disconnectpeer(msg):
        # return handle_request(
        #     squeak_admin_pb2.DisconnectPeerRequest(),
        #     handler.handle_disconnect_peer,
        # )
        return handler.handle_disconnect_peer(msg)

    @app.route("/getexternaladdress", methods=["POST"])
    @login_required
    @protobuf_serialized(squeak_admin_pb2.GetExternalAddressRequest())
    def getexternaladdress(msg):
        # return handle_request(
        #     squeak_admin_pb2.GetExternalAddressRequest(),
        #     handler.handle_get_external_address,
        # )
        return handler.handle_get_external_address(msg)

    return app


class SqueakAdminWebServer:
    def __init__(
        self,
        host,
        port,
        username,
        password,
        use_ssl,
        login_disabled,
        allow_cors,
        handler,
    ):
        self.host = host
        self.port = port
        self.use_ssl = use_ssl
        self.login_disabled = login_disabled
        self.allow_cors = allow_cors
        self.app = create_app(handler, username, password)
        self.server = None

    def get_app(self):

        # Set LOGIN_DISABLED and allow CORS if login not required.
        if self.login_disabled:
            self.app.config["LOGIN_DISABLED"] = True

        # Allow CORS
        if self.allow_cors:
            CORS(self.app)

        return self.app

    def start(self):
        self.server = make_server(
            self.host,
            self.port,
            self.get_app(),
            threaded=True,
            ssl_context="adhoc" if self.use_ssl else None,
        )

        logger.info("Starting SqueakAdminWebServer...")
        threading.Thread(
            target=self.server.serve_forever,
        ).start()

    def stop(self):
        if self.server is None:
            return
        logger.info("Stopping SqueakAdminWebServer....")
        self.server.shutdown()
        logger.info("Stopped SqueakAdminWebServer.")
