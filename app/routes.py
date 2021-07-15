from flask import request, redirect, render_template, url_for, Blueprint, Flask
from flask_login import login_required
from bson.objectid import ObjectId
from .db import db
from .db import get_db
import os

# app.config["dbDB_SETTINGS"] = {
#  "db": "peddlerdb",
#   "host": "dbdb://127.0.0.1:27017/peddlerdb",
# "SECRET_KEY": "os.getenv('any secret string')"
# }

############################################################
# SETUP
############################################################
main_bp = Blueprint('main', __name__)

# app.config["db_URI"] = "dbdb://127.0.0.1:27017/peddlerdb"

# mongo = PyMongo(app)
# db = MongoEngine(app)

############################################################
# ROUTES
############################################################


@main_bp.route('/')
def home():
    posts_data = db.posts.find({})

    context = {
        'posts': posts_data,
    }

    return render_template('home.html', **context)

# @login_required


@main_bp.route('/createpost', methods=["GET", "POST"])
@login_required
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
            # 'user_id': current_user.id,
            'post_url': post_url,
            'post_title': post_title,
            'location': location,
            'post_description': post_description,
            'post_long_description': post_long_description,
            'post_album': []

        }

        result = db.posts.insert_one(new_post)
        inserted_id = result.inserted_id
        for item in range(30):
            if request.form.get(f'{item}') == None:
                break
            elif request.form.get(f'{item}') != None:
                db.posts.update({"_id": ObjectId(result.inserted_id)},
                                      {
                    "$push": {"post_album": {"picture": request.form.get(f'{item}')}}
                })

        return redirect(url_for('main.detail', post_id=inserted_id))

    else:
        return render_template('create_post.html')


@ main_bp.route('/edit/<post_id>', methods=["GET", "POST"])
@login_required
def edit(post_id):
    if request.method == "POST":
        post_url = request.form.get('post_url')
        post_title = request.form.get('post_title')
        location = request.form.get('location')
        post_description = request.form.get('post_description')
        post_long_description = request.form.get('post_long_description')

        db.posts.update_one({
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

        post_to_show = db.posts.find_one({
            '_id': ObjectId(post_id)
        })

        context = {
            'post': post_to_show
        }

        return render_template('edit_post.html', **context)


@ main_bp.route('/post/<post_id>')
def detail(post_id):
    post_to_show = db.posts.find_one({
        '_id': ObjectId(post_id)
    })
    context = {
        'post_id': ObjectId(post_id),
        'post': post_to_show
    }
    return render_template('post_detail.html', **context)


@ main_bp.route('/album/<post_id>')
def album_detail(post_id):
    post_to_show = db.posts.find_one({
        '_id': ObjectId(post_id)
    })
    context = {
        'post_id': ObjectId(post_id),
        'post': post_to_show
    }
    return render_template('show_album.html', **context)


@ main_bp.route('/edit/album/<post_id>', methods=["GET", "POST"])
@login_required
def edit_album(post_id):
    if request.method == "POST":
        new_picture = request.form.get('new_picture')
        album_var = db.posts.find_one({
            '_id': ObjectId(post_id)
        })

        db.posts.update(
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

        post_to_show = db.posts.find_one({
            '_id': ObjectId(post_id)
        })

        context = {
            'post': post_to_show
        }

        return render_template('edit_album.html', **context)


@ main_bp.route('/delete/<post_id>', methods=['POST'])
@login_required
def delete(post_id):
    db.posts.delete_one({
        '_id': ObjectId(post_id)
    })

    return redirect(url_for('main.home'))
