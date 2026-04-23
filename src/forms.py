from wtforms import (StringField, PasswordField, SelectField, TextAreaField, FloatField)
from wtforms.fields import DateTimeLocalField 
from wtforms.validators import (DataRequired, Email, Length, EqualTo, NumberRange, Optional, ValidationError)
from flask_wtf import FlaskForm

class RegisterForm(FlaskForm):
    username =StringField('Username', validators=[DataRequired(), Length(min=3, max=80)])
    email = StringField('Email', validators=[DataRequired(), Email(), Length(max=120)])
    password = PasswordField('Password', validators=[DataRequired(), Length(min=8)])
    confirm = PasswordField('Confirm password', validators=[DataRequired(),
            EqualTo('password', message='Passwords must match')])

class LoginForm(FlaskForm):
    email = StringField('Email',
        validators=[DataRequired(), Email()])
    password = PasswordField('Password',
        validators=[DataRequired() ])
    
class SleepEntryForm(FlaskForm):
    bedtime = DateTimeLocalField('Bedtime', format='%Y-%m-%dT%H:%M', validators=[DataRequired()])
    wake_time = DateTimeLocalField('Wake time', format='%Y-%m-%dT%H:%M', validators=[DataRequired()])
    quality = SelectField('Quality', choices=[
        ('1','1 - Very Poor'), ('2', '2 - Poor'), ('3', '3 - Fair'), ('4', '4 - Good'), ('5','5 - Excellent')
    ])
    notes = TextAreaField('Notes', validators=[Optional(), Length(max=500)])

    def validate_wake_time(self, field):
        if self.bedtime.data and field.data:
            if field.data <= self.bedtime.data:
                raise ValidationError(
                    'Wake time must be after bedtime'
                )
class SleepGoalForm(FlaskForm):
    target_hours = FloatField('Target hours', validators=[DataRequired(), NumberRange(min=4, max=12)])