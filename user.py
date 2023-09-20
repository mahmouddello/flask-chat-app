from flask_login import UserMixin
from werkzeug.security import check_password_hash
from attrs import define


@define(kw_only=True)
class User(UserMixin):
    username: str
    email: str
    password: str

    # There is `id` attribute, so we have to override the methods from UserMixin
    def get_id(self) -> str:
        """
        Override default `id` attribute of UserMixin class.

        :return: String of username.
        """
        return self.username

    def check_password(self, password_input: str) -> bool:
        """
        Returns True if the passwords hash is identical, otherwise False.

        :param password_input: Password inputted by user.
        :return: Boolean (True or False).
        """
        return check_password_hash(pwhash=self.password, password=password_input)
