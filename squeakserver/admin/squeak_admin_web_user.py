from flask_login import UserMixin


class User(UserMixin):

    def is_authenticated(self):
        return True

    def is_active(self):
        return True

    def is_anonymous(self):
        return False

    def get_id(self):
        return "fake-user"
