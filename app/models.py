from flask_login import login_manager, UserMixin
from .db import get_db


class User(UserMixin, get_db.Document):
    username = get_db.StringField(max_length=30)
    password = get_db.StringField()

# @login_manager.user_loader
# def load_user(user_id):
#     return User.objects(pk=user_id).first()