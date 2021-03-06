
from wtforms import StringField, PasswordField, SubmitField, BooleanField, SelectField, IntegerField, \
    FileField, TextField, validators, RadioField, SelectMultipleField
from wtforms.widgets import TextArea
from wtforms.widgets import ListWidget, CheckboxInput
from flask_wtf import FlaskForm
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError, Regexp
from wtforms.fields.html5 import DateField
from wtforms.ext.sqlalchemy.fields import QuerySelectField
from wtforms_components import DateTimeField, DateRange
from flask_wtf.file import FileField, FileRequired
from werkzeug.utils import secure_filename
from flask_bcrypt import Bcrypt, generate_password_hash, check_password_hash
from datetime import datetime, date, timedelta
from flask import session
from wtforms.validators import NumberRange


class newSkater(FlaskForm):
    name = StringField('Skater Name', validators=[DataRequired(), Length(min=2, max=30)])
    DOB = StringField('Age', validators=[DataRequired(), Length(min=2, max=30)])
    nationality = StringField('Nationality', validators=[DataRequired(), Length(min=2, max=30)])
    gender = SelectField('Sex', choices=[('Male', 'Male'), ('Female', 'Female')])
    skateboard = StringField('Skateboard Company', validators=[DataRequired(), Length(min=2, max=30)])
    shoes = StringField('Shoe Sponsor', validators=(DataRequired(), Length(min=2, max=30)))
    trucks = StringField('Truck Sponsor', validators=[DataRequired(), Length(min=2, max=30)])
    wheels = StringField('Wheel  Sponsor', validators=[DataRequired(), Length(min=2, max=30)])
    submit = SubmitField('Propose new skater')

class search(FlaskForm):
    search = StringField('Search', validators=[DataRequired(), Length(min=3, max=30)])

class contactForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired(), Length(min=3, max=30)])
    emailAddress = StringField('Email', validators=[DataRequired(), Email()])
    message = TextField('Write your message here...', validators=[DataRequired(), Length(min=20, max=250)])

class loginForm(FlaskForm):
    username = StringField('username', validators=[DataRequired(), Length(min=2, max=30)])
    password = PasswordField('password', validators=[DataRequired(), Length(min=2, max=30)])
    submit = SubmitField('login')

class registration(FlaskForm):
    username = StringField('username', validators=[DataRequired(), Length(min=2, max=30)])
    password = PasswordField('password', validators=[DataRequired(), Length(min=2, max=30)])
    emailAddress = StringField('Email Address', validators=[DataRequired(), Email()])
    submit = SubmitField('Register')
