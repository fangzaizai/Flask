# -*- codind:utf-8 -*-
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField, BooleanField
from wtforms.validators import Required, Length, Email
 
class LoginForm(FlaskForm):
 	email = StringField('Email', validators=[Required(), Length(1, 64), Email()])
 	password = PasswordField('Password', validators=[Required()])
 	remember_me = BooleanField('Keep me logged in')
 	submit = SubmitField('Log In')
