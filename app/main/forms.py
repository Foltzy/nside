# forms.py
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SelectField, IntegerField
from wtforms.validators import InputRequired, Email, Length
from ..models import User

# check current emails and throw (err) if already in use
def check_email(form, field):
    input_email = field.data
    other_emails = User.query.filter_by(email=input_email).all()
     
    if len(other_emails) != 0:
        raise validators.ValidationError('That email is already in use!')  

class LoginForm(FlaskForm):
    email = StringField('email', validators=[InputRequired(), Email(message='Invalid email')])
    password = PasswordField('password', validators=[InputRequired(), Length(min=4, max=80)])

class RegisterForm(FlaskForm):
    first_name = StringField('first name', validators=[InputRequired()])
    last_name = StringField('last name', validators=[InputRequired()])
    email = StringField('email', validators=[InputRequired(), Email(message='Invalid email'), check_email])
    password = PasswordField('password', validators=[InputRequired(), Length(min=4, max=80)])
    room_id = SelectField('room', choices=[])

class ResidentOfForm(FlaskForm):
    room_id = SelectField('room', choices=[])
