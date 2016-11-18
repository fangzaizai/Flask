#-*- coding: utf-8 -*-
from flask_sqlalchemy import SQLAlchemy
from . import db, login_manager
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from flask import current_app

class Role(db.Model):
	__tablename__ = 'roles'
	id = db.Column(db.Integer, primary_key=True)
	name = db.Column(db.String(64), unique=True)
	users = db.relationship('User', backref='role', lazy='dynamic')  #?
	

	def __repr__(self):
		return '<Role %r>' % self.name

class User(UserMixin, db.Model):
	"""docstring for User"""
	__tablename__ = 'users'
	id = db.Column(db.Integer, primary_key=True)
	email = db.Column(db.String(64), unique=True, index=True)
	username = db.Column(db.String(64), unique=True, index=True)
	password_hash = db.Column(db.String(128))
	role_id = db.Column(db.Integer, db.ForeignKey('roles.id'))
	confirmed = db.Column(db.Boolean, default=False)
	#用于将对象打印出来，将属性和方法整理成一个可以打印输出的格式
	#def __repr__(self):
		#return '<User %r>' % self.username

	@property
	def password(self):
		raise AttributeError('password is not a readable attribute')

	@password.setter
	def password(self, password):
		self.password_hash = generate_password_hash(password)

	def verify_password(self, password):
		return check_password_hash(self.password_hash, password)

	#生成一个；令牌
	def generate_confirmation_token(self, expiration=3600):
		s = Serializer(current_app.config['SECRET_KEY'], expiration)
		return s.dumps({'confirm': self.id})

	#检验令牌
	def confirm(self, token):
		s=Serializer(current_app.config['SECRET_KEY'])
		try:
			data=s.loads(token)
		except:
			return False
		if data.get('confirm') != self.id:
			return False
		self.confirmed = True
		db.session.add(self)
		return True

@login_manager.user_loader
def load_user(user_id):
	#如果找到用户，返回用户对象，否则返回None
	return User.query.get(int(user_id))  
