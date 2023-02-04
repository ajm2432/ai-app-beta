

from flask_login import UserMixin
from flask import session

class Users(UserMixin):
    def get_user():
        username = session['username']
        return username

