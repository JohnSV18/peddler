from flask_login import login_manager, UserMixin
from flask_mongoengine import MongoEngine
from cyclick_app.main.routes import *


class User(UserMixin, db.Document):
    email = db.StringField(max_length=30)
    password = db.StringField()
