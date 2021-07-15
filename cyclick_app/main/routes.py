from flask import request, redirect, render_template, url_for, Blueprint, Flask
from flask_login import current_user
from bson.objectid import ObjectId
from flask_pymongo import PyMongo
from flask_mongoengine import MongoEngine
#from cyclick_app.auth.auth_routes import *
import os

app = Flask(__name__)
# app.config["MONGODB_SETTINGS"] = {
#  "db": "peddlerdb",
#   "host": "mongodb://127.0.0.1:27017/peddlerdb",
# "SECRET_KEY": "os.getenv('any secret string')"
# }

############################################################
# SETUP
############################################################
main = Blueprint('main', __name__)

# app.config["MONGO_URI"] = "mongodb://127.0.0.1:27017/peddlerdb"


host = os.environ.get("MONGODB_URI", "mongodb+srv://johndoe:12345@cyclick.h18wa.mongodb.net/peddlerdb") + "?retryWrites=false"
app.config["MONGO_URI"] = host
mongo = PyMongo(app)
db = MongoEngine(app)

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

# @login_required


@main.route('/createpost', methods=["GET", "POST"])
def create():
    post_url = request.form.get('post_url')
    post_title = request.form.get('post_title')
    location = request.form.get('location')
    post_description = request.form.get('post_description')
    post_long_description = request.form.get('post_long_description')
    counter = 0
    pictureArr = []
    for item in range(30):
        if request.form.get(f'{item}') == None:
            break
        elif request.form.get(f'{item}') != None:
            pictureArr.append(request.form.get(f'{item}'))

    if request.method == 'POST':
        new_post = {
            'user_id': current_user.get_id(),
            'post_url': post_url,
            'post_title': post_title,
            'location': location,
            'post_description': post_description,
            'post_long_description': post_long_description,
            'post_album': []

        }

        result = mongo.db.posts.insert_one(new_post)
        inserted_id = result.inserted_id
        for item in range(30):
            if request.form.get(f'{item}') == None:
                break
            elif request.form.get(f'{item}') != None:
                mongo.db.posts.update({"_id": ObjectId(result.inserted_id)},
                                      {
                    "$push": {"post_album": {"picture": request.form.get(f'{item}')}}
                })

        return redirect(url_for('main.detail', post_id=inserted_id))

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
                'post_url': post_url,
                'post_title': post_title,
                'location': location,
                'post_description': post_description,
                'post_long_description': post_long_description,

            }
        })

        return redirect(url_for('main.detail', post_id=post_id))
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


@ main.route('/album/<post_id>')
def album_detail(post_id):
    post_to_show = mongo.db.posts.find_one({
        '_id': ObjectId(post_id)
    })
    context = {
        'post_id': ObjectId(post_id),
        'post': post_to_show
    }
    return render_template('show_album.html', **context)


@ main.route('/edit/album/<post_id>', methods=["GET", "POST"])
def edit_album(post_id):
    if request.method == "POST":
        new_picture = request.form.get('new_picture')
        album_var = mongo.db.posts.find_one({
            '_id': ObjectId(post_id)
        })

        mongo.db.posts.update(
            {"_id": ObjectId(post_id)},
            {
                "$push": {
                    "post_album": {"picture": new_picture}
                }
            })

        context = {
            "post": album_var
        }

        # return render_template('show_album.html', **context)
        return redirect(url_for('main.album_detail', post_id=post_id))
    else:

        post_to_show = mongo.db.posts.find_one({
            '_id': ObjectId(post_id)
        })

        context = {
            'post': post_to_show
        }

        return render_template('edit_album.html', **context)


@ main.route('/delete/<post_id>', methods=['POST'])
def delete(post_id):
    mongo.db.posts.delete_one({
        '_id': ObjectId(post_id)
    })

    return redirect(url_for('main.home'))