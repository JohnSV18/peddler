import re
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

@main.route('/createpost', methods=["GET", "POST"])
def create():
    post_title = request.form.get('post_title')
    location = request.form.get('location')    
    post_description = request.form.get('post_description')
    post_long_description = request.form.get('post_long_description')

    if request.method == 'POST':
        new_post = {
            'post_title' : post_title,
            'location' : location,
            'post_description': post_description,
            'post_long_description': post_long_description
    
        }
       
        result=mongo.db.workouts_data.insert_one(new_post)
        inserted_id = result.inserted_id

        return redirect(url_for('detail', post_id=inserted_id))

    else:
        return render_template('createpost.html')

@main.route('/edit/<post_id>', methods=["GET", "POST"])
def edit(post_id):
    if request.method == "POST":
        post_title = request.form.get('post_title')
        location = request.form.get('location')
        post_description = request.form.get('post_description')
        post_long_description = request.form.get('post_long_description')
        

        mongo.db.workouts_data.update_one({
            '_id': ObjectId(post_id),
            
        },
        {
            '$set': {
                '_id': ObjectId(post_id),
                'post_title' : post_title,
                'location' : location,
                'post_description': post_description,
                'post_long_description': post_long_description
            }
        })

        return redirect(url_for('detail', post_id=post_id))
    else:

        post_to_show=mongo.db.posts_data.find_one({
            '_id': ObjectId(post_id)
        })

        context = {
            'post': post_to_show
        }

        return render_template('edit.html', **context)