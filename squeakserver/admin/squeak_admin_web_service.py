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

    @app.route('/getfollowedsqueakdisplays', methods=["POST"])
    def getfollowedsqueakdisplays():
        data = request.get_data()
        req = squeak_admin_pb2.GetFollowedSqueakDisplaysRequest()
        req.ParseFromString(data)
        reply = handler.handle_get_followed_squeak_display_entries()
        reply_data = reply.SerializeToString(reply)
        return reply_data

    @app.route('/setsqueakprofilesharing', methods=["POST"])
    def setsqueakprofilesharing():
        data = request.get_data()
        req = squeak_admin_pb2.SetSqueakProfileSharingRequest()
        req.ParseFromString(data)
        profile_id = req.profile_id
        sharing = req.sharing
        reply = handler.handle_set_squeak_profile_sharing(profile_id, sharing)
        reply_data = reply.SerializeToString(reply)
        return reply_data

    @app.route('/lndgetinfo', methods=["POST"])
    def lndgetinfo():
        data = request.get_data()
        req = lnd_pb2.GetInfoRequest()
        req.ParseFromString(data)
        reply = handler.handle_lnd_get_info()
        reply_data = reply.SerializeToString(reply)
        return reply_data

    @app.route('/lndwalletbalance', methods=["POST"])
    def lndwalletbalance():
        data = request.get_data()
        req = lnd_pb2.WalletBalanceRequest()
        req.ParseFromString(data)
        reply = handler.handle_lnd_wallet_balance()
        reply_data = reply.SerializeToString(reply)
        return reply_data

    return app


def run_app(handler):
    app = create_app(handler)
    app.run(
        host="0.0.0.0",
        port=5000,
        debug=False,
    )
