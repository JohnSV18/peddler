from flask import Flask
from flask_login import LoginManager, login_manager
from flask_mongoengine import MongoEngine
# from cyclick_app.main.routes import main
from .models import User
from .auth.auth_routes import auth
from .main.routes import main
from flask_mongoengine import MongoEngine
import os

db = MongoEngine()
def init_app():
    app = Flask(__name__)
    app.secret_key = os.urandom(24)
    app.config["MONGODB_SETTINGS"] = {
        "db": "peddlerdb",
        "host": "mongodb://127.0.0.1:27017/peddlerdb", 
        "connect": True
    }
    

    
    with app.app_context():
        # login_manager = LoginManager()
        # login_manager.init_app(app) 
        # login_manager.login_view = 'users.login'
        db.init_app(app)
        app.register_blueprint(main)
        app.register_blueprint(auth)
    return app



#  

# from flask_login import LoginManager
# login_manager = LoginManager()
# login_manager.login_view = "auth.login"
# login_manager.init_app(app)

# from cyclick_app.auth.models import User

# @login_manager.user_loader
# def load_user(user_id):
#     return User.objects(pk=user_id).first()
