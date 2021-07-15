from flask_login import UserMixin
from cyclick_app.main.routes import db


class User(UserMixin, db.Document):
    username = db.StringField(max_length=30)
    password = db.StringField()