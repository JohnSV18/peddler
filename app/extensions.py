from flask import Flask

from flask_pymongo import PyMongo
from flask_login import LoginManager
from flask_bcrypt import Bcrypt
# from app.config import Config
import os

app = Flask(__name__)

