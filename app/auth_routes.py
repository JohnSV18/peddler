from flask import Blueprint, request, render_template, redirect, url_for
from flask_login import login_required, login_user, logout_user, current_user
from .models import User
from . import SignUpForm, LoginForm
from werkzeug.security import generate_password_hash, check_password_hash
from app.db import get_db

bp = Blueprint('auth', __name__, url_prefix='/auth')

@bp.route('/signup', methods=['GET', 'POST'])
def register():
    form = SignUpForm()
    if request.method == 'POST':
        if form.validate_on_submit():
            existing_user = User.objects(username=form.username.data).first()
            if existing_user is None:
                hashpass = generate_password_hash(
                    form.password.data, method='sha256')
                user = User(username=form.username.data,
                            password=hashpass).save()
                # login_user(user)
                return redirect(url_for('auth.authenticated'))

    return render_template('signup.html', form=form)


@bp.route('/authenticated')
@login_required
def authenticated():
    return render_template('home.html', name=current_user.username)
# @auth.route('/signup', methods=['GET', 'POST'])
# def signup():
#     if request.method == 'POST':
#         users = mongo.db.users
#         existing_user = users.find_one({'name' : request.form['username']})
#         if existing_user is None:
#             hashpass = bycrypt.hashpw(request.form['password'], bycrypt.genSalt())
#             users.insert({'name' : request.form['username'], 'password': hashpass})
#             session['username'] = request.form['username']
#             return redirect(url_for('main.home'))
#         return 'That username already exists!'
#     return render_template('signup.html')


@bp.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated == True:
        return redirect(url_for('main.home'))
    form = LoginForm()
    if request.method == 'POST':
        if form.validate_on_submit():
            check_user = User.objects(username=form.username.data).first()
            if check_user:
                if check_password_hash(check_user['password'], form.password.data):
                    login_user(check_user)
                    return redirect(url_for('main.home'))
    return render_template('login.html', form=form)

@bp.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('main.home'))
    # return render_template('home.html', name=current_user.email)
