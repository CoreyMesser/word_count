from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import DataRequired, ValidationError, Email, EqualTo
from word_data.models import User
from word_data.services import DatabaseServices


class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Remember Me')
    submit = SubmitField('Sign In')


class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    password2 = PasswordField(
        'Repeat Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Register')

    def validate_username(self, username):
        ds = DatabaseServices()
        user = ds.get_user(username=username)
        if user is not None:
            raise ValidationError('Please use a different username.')

    def validate_email(self, email):
        ds = DatabaseServices()
        user = user = ds.get_email(email=email)
        if user is not None:
            raise ValidationError('Please use a different email address.')
