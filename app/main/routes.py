from flask import Flask, request, redirect, render_template, url_for, Blueprint
from flask_pymongo import PyMongo
from jinja2 import Template

from bson.objectid import ObjectId
import pymongo
# import dns
import os

############################################################
# SETUP
############################################################
app = Flask(__name__)
main = Blueprint('main', __name__)

app.config["MONGO_URI"] = "mongodb://127.0.0.1:27017/peddlerdb"

mongo = PyMongo(app)

############################################################
# ROUTES
############################################################


@main.route('/')
def home():
    posts_data = mongo.db.posts.find({})

    context = {
        'posts': posts_data,
    }

    return render_template('home.html', **context)
