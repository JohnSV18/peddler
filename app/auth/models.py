from app import mongo
from flask_login import UserMixin, login_manager

class User(UserMixin, mongo.Document):
    meta = {'collection': '<---YOUR_COLLECTION_NAME--->'}
    email = mongo.StringField(max_length=30)
    password = mongo.StringField()
@login_manager.user_loader
def load_user(user_id):
    return User.objects(pk=user_id).first()