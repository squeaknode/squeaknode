import logging

from flask_login import UserMixin

from werkzeug.security import generate_password_hash, check_password_hash


logger = logging.getLogger(__name__)


class User(UserMixin):

    def __init__(self, username, password):
        self.username = username
        logger.info("Generating hash for password: {}".format(password))
        self.password_hash = generate_password_hash(password)
        logger.info("Generated hash: {}".format(self.password_hash))

    def is_authenticated(self):
        return True

    def is_active(self):
        return True

    def is_anonymous(self):
        return False

    def get_id(self):
        return self.username

    def check_password(self, password):
        logger.info("Checking password: {}".format(password))
        check_passed = check_password_hash(self.password_hash, password)
        logger.info("Did password check succeed?: {}".format(check_passed))
        return check_password_hash(self.password_hash, password)

    def get_user_by_username(self, username):
        if self.username == username:
            return self
