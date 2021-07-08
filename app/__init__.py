from app.main.routes import main
from flask import Flask
import os

app = Flask(__name__)

app.register_blueprint(main)
