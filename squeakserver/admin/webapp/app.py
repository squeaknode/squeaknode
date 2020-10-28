import os
from os.path import abspath, dirname
import logging

from flask import Flask
from flask import request
from flask import redirect, url_for
from flask import render_template
from flask import flash

from flask_login import LoginManager
from flask_login import current_user, login_user
from flask_login import login_required
from flask_login import logout_user

from google.protobuf import json_format
from google.protobuf import message

from proto import squeak_admin_pb2, squeak_admin_pb2_grpc
from proto import lnd_pb2, lnd_pb2_grpc

from squeakserver.admin.webapp.squeak_admin_web_user import User
from squeakserver.admin.webapp.forms import LoginForm

logger = logging.getLogger(__name__)


def create_app(handler, username, password):
    # create and configure the app
    logger.info("Starting flask app from directory: {}".format(os.getcwd()))
    # root_path = 'squeakserver/admin/webapp'
    # root_path = os.path.dirname(os.path.realpath(__file__))
    #logger.info("Starting flask with root_path: {}".format(root_path))
    # readme = open("README.md", "r").read()
    # logger.info("Starting flask with README: {}".format(readme))
    # base_template = open("squeakserver/admin/webapp/templates/base.html", "r").read()
    # logger.info("Starting flask with template: {}".format(base_template))
    app = Flask(
        __name__,
        static_folder='static/build',
        #static_url_path='/',
        # template_folder='templates',
        # root_path=root_path,
    )
    app.config.from_mapping(
        SECRET_KEY='dev',
    )
    login = LoginManager(app)
    valid_user = User(
        username,
        password,
    )
    logger.info("Starting flask with app.root_path: {}".format(app.root_path))
    logger.info("Files in root path: {}".format(os.listdir(app.root_path)))
    other_path = abspath(dirname(__file__))
    logger.info("Starting flask other_path: {}".format(other_path))
    logger.info("template folder: {}".format(app.template_folder))
    # logger.info("Files in template folder: {}".format(os.listdir(app.template_folder)))


    @login.user_loader
    def load_user(id):
        return valid_user.get_user_by_username(id)

    @login.unauthorized_handler
    def unauthorized_callback():
        return redirect('/login')

    def handle_request(request_message, handle_rpc_request):
        data = request.get_data()
        request_message.ParseFromString(data)
        reply = handle_rpc_request(request_message)
        return reply.SerializeToString(reply)

    @app.route('/login', methods=['GET', 'POST'])
    def login():
        logger.info("Trying to login")
        if current_user.is_authenticated:
            return redirect(url_for('index'))
        form = LoginForm()
        if form.validate_on_submit():
            user = valid_user.get_user_by_username(form.username.data)
            if user is None or not user.check_password(form.password.data):
                flash('Invalid username or password')
                return redirect(url_for('login'))
            login_user(user, remember=form.remember_me.data)
            return redirect(url_for('index'))
        return render_template('login.html', title='Sign In', form=form)

    @app.route('/logout')
    def logout():
        logout_user()
        return redirect(url_for('index'))

    @app.route('/')
    @login_required
    def index():
        logger.info("Getting index route.")
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

    @app.route('/lndnewaddress', methods=["POST"])
    def lndnewaddress():
        return handle_request(
            lnd_pb2.NewAddressRequest(),
            handler.handle_lnd_new_address,
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

    @app.route('/makesqueakrequest', methods=["POST"])
    def makesqueakrequest():
        return handle_request(
            squeak_admin_pb2.MakeSqueakRequest(),
            handler.handle_make_squeak,
        )

    @app.route('/getsqueakdisplay', methods=["POST"])
    def getsqueakdisplay():
        return handle_request(
            squeak_admin_pb2.GetSqueakDisplayRequest(),
            handler.handle_get_squeak_display_entry,
        )

    @app.route('/getancestorsqueakdisplays', methods=["POST"])
    def getancestorsqueakdisplays():
        return handle_request(
            squeak_admin_pb2.GetAncestorSqueakDisplaysRequest(),
            handler.handle_get_ancestor_squeak_display_entries,
        )

    @app.route('/getsqueakprofilebyaddress', methods=["POST"])
    def getsqueakprofilebyaddress():
        return handle_request(
            squeak_admin_pb2.GetSqueakProfileByAddressRequest(),
            handler.handle_get_squeak_profile_by_address,
        )

    @app.route('/getaddresssqueakdisplays', methods=["POST"])
    def getaddresssqueakdisplays():
        return handle_request(
            squeak_admin_pb2.GetAddressSqueakDisplaysRequest(),
            handler.handle_get_squeak_display_entries_for_address,
        )

    @app.route('/createcontactprofile', methods=["POST"])
    def createcontactprofile():
        return handle_request(
            squeak_admin_pb2.CreateContactProfileRequest(),
            handler.handle_create_contact_profile,
        )

    @app.route('/createsigningprofile', methods=["POST"])
    def createsigningprofile():
        return handle_request(
            squeak_admin_pb2.CreateSigningProfileRequest(),
            handler.handle_create_signing_profile,
        )

    @app.route('/createpeer', methods=["POST"])
    def createpeer():
        return handle_request(
            squeak_admin_pb2.CreatePeerRequest(),
            handler.handle_create_peer,
        )

    @app.route('/deletepeer', methods=["POST"])
    def deletepeer():
        return handle_request(
            squeak_admin_pb2.DeletePeerRequest(),
            handler.handle_delete_squeak_peer,
        )

    @app.route('/deleteprofile', methods=["POST"])
    def deleteprofile():
        return handle_request(
            squeak_admin_pb2.DeleteSqueakProfileRequest(),
            handler.handle_delete_squeak_profile,
        )

    @app.route('/deletesqueak', methods=["POST"])
    def deletesqueak():
        return handle_request(
            squeak_admin_pb2.DeleteSqueakRequest(),
            handler.handle_delete_squeak,
        )

    return app


class SqueakAdminWebServer():

    def __init__(self, host, port, username, password, use_ssl, handler):
        self.host = host
        self.port = port
        self.use_ssl = use_ssl
        self.app = create_app(handler, username, password)

    def serve(self):
        self.app.run(
            self.host,
            self.port,
            debug=False,
            ssl_context='adhoc' if self.use_ssl else None,
        )
