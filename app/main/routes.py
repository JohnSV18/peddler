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
    post_url = request.form.get('post_url')
    post_title = request.form.get('post_title')
    location = request.form.get('location')
    post_description = request.form.get('post_description')
    post_long_description = request.form.get('post_long_description')

    if request.method == 'POST':
        new_post = {
            'post_url': post_url,
            'post_title': post_title,
            'location': location,
            'post_description': post_description,
            'post_long_description': post_long_description,
            'post_album': {"picture": ""}

        }

        result = mongo.db.posts.insert_one(new_post)
        inserted_id = result.inserted_id

        return render_template('post_detail.html', post_id=inserted_id)

    else:
        return render_template('create_post.html')


@ main.route('/edit/<post_id>', methods=["GET", "POST"])
def edit(post_id):
    if request.method == "POST":
        post_url = request.form.get('post_url')
        post_title = request.form.get('post_title')
        location = request.form.get('location')
        post_description = request.form.get('post_description')
        post_long_description = request.form.get('post_long_description')

        mongo.db.posts.update_one({
            '_id': ObjectId(post_id),

        },
            {
            '$set': {
                '_id': ObjectId(post_id),
                'post_url' : post_url,
                'post_title': post_title,
                'location': location,
                'post_description': post_description,
                'post_long_description': post_long_description,

            }
        })

        return redirect(url_for('post_detail', post_id=post_id))
    else:

        post_to_show = mongo.db.posts.find_one({
            '_id': ObjectId(post_id)
        })

        context = {
            'post': post_to_show
        }

        return render_template('edit_post.html', **context)


@ main.route('/post/<post_id>')
def detail(post_id):
    post_to_show = mongo.db.posts.find_one({
        '_id': ObjectId(post_id)
    })
    context = {
        'post_id': ObjectId(post_id),
        'post': post_to_show
    }
    return render_template('post_detail.html', **context)


@ main.route('/edit/album/<post_id>', methods=["GET", "POST"])
def edit_album(post_id):
    if request.method == "POST":
        new_picture = request.form.get('new_picture')
        album_var = mongo.db.posts.find_one({
            '_id': ObjectId(post_id)
        })

        mongo.db.posts.update({"_id": ObjectId(post_id)},
                              {
            "$push": {"post_album": {"picture": new_picture}}
        })

        context = {
            "post": album_var
        }

        return render_template('show_album.html', **context)
    else:

        post_to_show = mongo.db.posts.find_one({
            '_id': ObjectId(post_id)
        })

        context = {
            'post': post_to_show
        }

        return render_template('edit_album.html', **context)


@ app.route('/delete/<post_id>', methods=['POST'])
def delete(post_id):
    mongo.db.workouts_data.delete_one({
        '_id': ObjectId(post_id)
    })

    return render_template('home.html')
