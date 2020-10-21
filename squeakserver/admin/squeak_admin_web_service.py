import os
import logging

from flask import Flask
from flask import request

from google.protobuf import json_format


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
        logger.info("Getting getfollowedsqueakdisplays route.")
        data = request.get_data()
        logger.info("Request data: {}".format(data))

        reply = handler.handle_get_followed_squeak_display_entries()
        logger.info("reply: {}".format(reply))
        reply_data = reply.SerializeToString(reply)
        logger.info("reply_data: {}".format(reply_data))
        return reply_data

    return app


def run_app(handler):
    app = create_app(handler)
    app.run(
        host="0.0.0.0",
        port=5000,
        debug=False,
    )
