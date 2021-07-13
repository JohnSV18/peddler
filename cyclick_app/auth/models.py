from flask_login import login_manager, UserMixin
from flask_mongoengine import MongoEngine
from cyclick_app.main.routes import mongo


class User(UserMixin, MongoEngine.Document):
    email = MongoEngine.StringField(max_length=30)
    password = MongoEngine.StringField()
    
