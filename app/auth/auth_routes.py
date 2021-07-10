from flask import Blueprint, request, render_template, redirect, url_for, flash
from app.auth.models import User
from app.auth.forms import SignUpForm
from flask_login import login_required, login_user, logout_user, current_user
from flask_bcrypt import Bcrypt
from app import app, mongo
from werkzeug.security import generate_password_hash, check_password_hash

auth = Blueprint('auth', __name__)
bycrypt = Bcrypt(app)

@auth.route('/signup', methods=['GET', 'POST'])
def signup():
    form = SignUpForm()
    if request.method == 'POST':
        if form.validate():
            existing_user = User.objects(username=form.username.data).first()
            if existing_user is None:
                hashpass = generate_password_hash(form.password.data, method='sha256')
                hey = User(form.username.data,hashpass).save()
                login_user(hey)
                return redirect(url_for('main.home'))
    return render_template('signup.html', form=form)

@auth.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated == True:
        return redirect(url_for('main.home'))
    form = SignUpForm()
    if request.method == 'POST':
        if form.validate():
            check_user = User.objects(email=form.email.data).first()
            if check_user:
                if check_password_hash(check_user['password'], form.password.data):
                    login_user(check_user)
                    return redirect(url_for('main.home'))
    return render_template('login.html', form=form)

@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('main.home'))
    # return render_template('home.html', name=current_user.email)