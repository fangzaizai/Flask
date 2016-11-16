# -*-coding:utf-8-*-
import os

basedir = os.path.abspath(os.path.dirname(__file__))

class Config:
	SECRET_KEY = os.environ.get('SECRET_KEY') or 'derfqhLWXfrefjiqdw,?RT'
	SQLALCHEMY_COMMIT_ON_TEARDOWN = True
	SQLALCHEMY_TRACK_MODIFICATIONS =True
	FLASKY_MAIL_SUBJECT_PREFIX='[Flasky]'
	FLASKY_MAIL_SENDER = 'Flasky Admin <1204089513@qq.com>'
	FLASKY_ADMIN = os.environ.get('FLASKY_ADMIN')

	@staticmethod
	def init_app(app):
		pass

class DevelopmentConfig(Config):
	DEBUG = True
	MAIL_SERVER = 'smtp.googlemail.com'
	MAIL_PORT = 587
	MAIL_USE_TLS = True
	MAIL_USERNAME = os.environ.get('MAIL_USERNAME')
	MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD')
	SQLALCHEMY_DATABASE_URI = 'postgresql://postgres:admin@localhost/amfang'

class TestingConfig(Config):
	TESTING = True
	SQLALCHEMY_DATABASE_URI = 'postgresql://postgres:admin@localhost/amfang'

class ProductionConfig(Config):
	SQLALCHEMY_DATABASE_URI = 'postgresql://postgres:admin@localhost/amfang'

config = {
	'development':DevelopmentConfig,
	'testing':TestingConfig,
	'production':ProductionConfig,

	'default': DevelopmentConfig
}
