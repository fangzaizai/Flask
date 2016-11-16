# -*- coding: utf-8 -*-
from flask import Flask,render_template
from flask_bootstrap import Bootstrap
from flask_moment import Moment
from flask_mail import Mail,Message
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
import os
os.chdir='C:/Users/amf/OneDrive/code/python/goto_falsk/new-flask'
from config import config

mail=Mail()
#程序实例作为参数传递给构造函数，初始化主类的实例，得到一个扩展类的对象
bootstrap = Bootstrap()
moment = Moment()
db= SQLAlchemy()
login_manager = LoginManager()
login_manager.session_protection = 'strong' #安全等级 None basic strong
login_manager.login_view = 'auth.login'   #定义路由端点

def create_app(config_name):
	app = Flask(__name__)
	app.config.from_object(config[config_name])
	config[config_name].init_app(app)

	bootstrap.init_app(app)
	moment.init_app(app)
	mail.init_app(app)
	db.init_app(app)
	login_manager.init_app(app)

	
	from .main import main as main_blueprint
	app.register_blueprint(main_blueprint)

	from .auth import auth as auth_blueprint
	app.register_blueprint(auth_blueprint, url_prefix='/auth')   #路由端点

	return app

