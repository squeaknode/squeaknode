import logging
import os
import threading

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

from squeaknode.admin.webapp.forms import LoginForm
from squeaknode.admin.webapp.squeak_admin_web_user import User

logger = logging.getLogger(__name__)


def create_app(handler, username, password):
    # create and configure the app
    logger.info("Starting flask app from directory: {}".format(os.getcwd()))
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
    logger.info("Starting flask with app.root_path: {}".format(app.root_path))
    logger.info("Files in root path: {}".format(os.listdir(app.root_path)))

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

    @app.route("/login", methods=["GET", "POST"])
    def login():
        logger.info("Trying to login")
        if current_user.is_authenticated:
            return redirect(url_for("index"))
        form = LoginForm()
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

        # self.app.run(
        #     self.host,
        #     self.port,
        #     debug=False,
        #     ssl_context="adhoc" if self.use_ssl else None,
        # )

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
