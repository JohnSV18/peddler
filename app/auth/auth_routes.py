from flask import Blueprint, request, render_template, redirect, url_for, flash, Flask
from auth.models import User
from auth.forms import SignUpForm
from flask_login import login_required, login_user, logout_user, current_user
from flask_bcrypt import Bcrypt
from app import app, mongo

auth = Blueprint('auth', __name__)
bycrypt = Bcrypt(app)

@app.route('/register', methods=['GET', 'POST'])
def register():
    form = SignUpForm()
    if request.method == 'POST':
        if form.validate():
            existing_user = User.objects(email=form.email.data).first()
            if existing_user is None:
                hashpass = generate_password_hash(form.password.data, method='sha256')
                hey = User(form.email.data,hashpass).save()
                login_user(hey)
                return redirect(url_for('home'))
    return render_template('signup.html', form=form)