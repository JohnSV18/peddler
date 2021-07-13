from ..database.db import db
from flask_login import UserMixin, login_manager


class User(UserMixin, db.Document):
    username = db.StringField(max_length=30)
    password = db.StringField(required=True)
    
    
# @login_manager.user_loader
# def load_user(user_id):
#     return User.get(user_id)