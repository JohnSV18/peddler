from app.main.routes import main
from app.auth.auth_routes import auth
from flask import Flask
import os

app = Flask(__name__)

app.register_blueprint(main)
app.register_blueprint(auth)
