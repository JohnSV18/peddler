from flask_login import LoginManager
from flask_bcrypt import Bcrypt
from books_app.config import Config
import os

app = Flask(__name__)
app.config.from_object(Config)
