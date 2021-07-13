from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField
from wtforms.validators import Length, URL, InputRequired, ValidationError
from cyclick_app.auth.models import User

class SignUpForm(FlaskForm):
    # email = StringField('email',  validators=[InputRequired(), Email(message='Invalid email'), Length(max=30)])
    # password = PasswordField('password', validators=[InputRequired(), Length(min=8, max=20)])
    username = StringField('User Name', validators=[InputRequired(), Length(min=3, max=50)])
    password = PasswordField('Password', validators=[InputRequired()])
    # # submit = SubmitField('Sign Up')

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError('That username is taken. Please choose a different one.')


# class LoginForm(FlaskForm):
#     username = StringField('User Name', validators=[DataRequired(), Length(min=3, max=50)])
#     password = PasswordField('Password', validators=[DataRequired()])
#     submit = SubmitField('Log In')
