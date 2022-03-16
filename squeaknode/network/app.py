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

from flask import Flask
from flask import jsonify
from flask import request
from werkzeug.serving import make_server

logger = logging.getLogger(__name__)


def create_app(handler):
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
    logger.debug("Starting flask with app.root_path: {}".format(app.root_path))
    logger.debug("Files in root path: {}".format(os.listdir(app.root_path)))

    @app.route("/")
    def index():
        logger.info("Getting index route.")
        return "Hello, Index!"

    @app.route("/hello")
    def hello_world():
        logger.info("Getting hello route.")
        return "Hello, World!"

    @app.route('/squeak/<hash>')
    def squeak(hash):
        logger.info("Getting squeak route.")
        logger.info(hash)
        squeak_bytes = handler.handle_get_squeak_bytes(hash)
        logger.info(squeak_bytes)
        return squeak_bytes

    @app.route("/lookup")
    def lookup():
        logger.info("Getting lookup route.")
        min_block = request.args.get('minblock')
        max_block = request.args.get('maxblock')
        pubkeys = request.args.getlist('pubkeys')
        logger.info("Hello, lookup! Min block {}, Max block {}, pubkeys: {}".format(
            min_block,
            max_block,
            pubkeys,
        ))
        squeak_hashes = handler.handle_lookup_squeaks(
            pubkeys,
            min_block,
            max_block,
        )
        squeak_hashes_str = [
            squeak_hash.hex()
            for squeak_hash in squeak_hashes
        ]
        logger.info(squeak_hashes_str)
        return jsonify(squeak_hashes_str)

    # @app.route("/gettimelinesqueakdisplays", methods=["POST"])
    # @protobuf_serialized(squeak_admin_pb2.GetTimelineSqueakDisplaysRequest())
    # def gettimelinesqueakdisplays(msg):
    #     return handler.handle_get_timeline_squeak_display_entries(msg)

    return app


class SqueakPeerWebServer:
    def __init__(
        self,
        host,
        port,
        handler,
    ):
        self.host = host
        self.port = port
        self.app = create_app(handler)
        self.server = None

    def get_app(self):
        return self.app

    def start(self):
        self.server = make_server(
            self.host,
            self.port,
            self.get_app(),
            threaded=True,
            ssl_context=None,
        )

        logger.info("Starting SqueakPeerWebServer...")
        threading.Thread(
            target=self.server.serve_forever,
        ).start()

    def stop(self):
        if self.server is None:
            return
        logger.info("Stopping SqueakPeerWebServer....")
        self.server.shutdown()
        logger.info("Stopped SqueakPeerWebServer.")
