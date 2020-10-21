import os
import logging

from flask import Flask


logger = logging.getLogger(__name__)


logger.info("Starting flask app from directory: {}".format(os.getcwd()))
app = Flask(__name__, static_folder='/app/static/build', static_url_path='/')


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


def run_app():
    app.run(
        host="0.0.0.0",
        port=5000,
        debug=False,
    )
