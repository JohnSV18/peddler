from app.main.routes import mongo
from flask_login import UserMixin, login_manager

class User(UserMixin, mongo.db.Document):
    meta = {'collection': 'Users'}
    email = mongo.db.StringField(max_length=30)
    password = mongo.db.StringField()
@login_manager.user_loader
def load_user(user_id):
    return User.objects(pk=user_id).first()