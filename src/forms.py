from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField
from wtforms.validators import (DataRequired,Email, Length, EqualTo)

class RegisterForm(FlaskForm):
    username =StringField('Username',
        validators=[DataRequired(), Length(min=3, max=80)])
    email = StringField('Email',
        validators=[DataRequired(), Email(), Length(max=120)])
    password = PasswordField('Password',
        validators=[DataRequired(), Length(min=8)])
    confirm = PasswordField('Confirm password',
        validators=[DataRequired(),
            EqualTo('password', message='Passwords must match')])

class LoginForm(FlaskForm):
    email = StringField('Email',
        validators=[DataRequired(), Email()])
    password = PasswordField('Password',
        validators=[DataRequired() ])
    