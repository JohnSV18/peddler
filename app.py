from flask import Flask, request, redirect, render_template, url_for
from flask_pymongo import PyMongo

from bson.objectid import ObjectId
import pymongo
import dns
import os

############################################################
# SETUP
############################################################
app = Flask(__name__)
# host = os.environ.get(
# 'MONGODB_URI', '') + "?retryWrites=false"

app.config["MONGO_URI"] = "mongodb://127.0.0.1:27017/peddlerdb"
#app.config["MONGO_URI"] = host

mongo = PyMongo(app)

############################################################
# ROUTES
############################################################
