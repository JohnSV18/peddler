from flask import Flask
from cyclick_app.main.routes import main
from cyclick_app.auth.auth_routes import auth

app = Flask(__name__)
app.register_blueprint(main)
app.register_blueprint(auth)


from flask_login import LoginManager
login_manager = LoginManager()
login_manager.login_view = "auth.login"
login_manager.init_app(app)

from cyclick_app.auth.models import User

@login_manager.user_loader
def load_user(user_id):
    return User.objects(pk=user_id).first()
