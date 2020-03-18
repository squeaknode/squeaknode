import os

from configparser import ConfigParser

from flask import Flask


def create_app(test_config=None):
    """Create and configure an instance of the Flask application."""
    app = Flask(__name__, instance_relative_config=True)

    config = ConfigParser()
    config.read(os.environ.get('MY_APP_CONFIG_FILE'))

    print(dict(config['flask']))

    flask_config = {k.upper():v for k,v in dict(config['flask']).items()}
    print(flask_config)
    app.config.from_mapping(
        **flask_config,
    )

    if test_config is None:
        # load the instance config, if it exists, when not testing
        app.config.from_pyfile("config.py", silent=True)
    else:
        # load the test config if passed in
        app.config.update(test_config)

    # ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    @app.route("/hello")
    def hello():
        return "Hello, World!"

    # register the database commands
    from squeaknode.server import db

    db.init_app(app)

    # apply the blueprints to the app
    from squeaknode.server import blog

    # Not using auth anymore.
    # app.register_blueprint(auth.bp)

    app.register_blueprint(blog.bp)

    # make url_for('index') == url_for('blog.index')
    # in another app, you might define a separate main index here with
    # app.route, while giving the blog blueprint a url_prefix, but for
    # the tutorial the blog will be the main index
    app.add_url_rule("/", endpoint="index")

    return app
