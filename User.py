#-*- coding: utf-8 -*-

from flask import current_app
from flask_bootstrap import Bootstrap
from flask import Flask,render_template,session,redirect,url_for,flash
from flask_moment import Moment
from datetime import datetime
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import Required
from flask_sqlalchemy import SQLAlchemy
from flask_script import Shell,Manager
from flask_migrate import Migrate, MigrateCommand
from flask_mail import Mail,Message

class NameForm(FlaskForm):
	name = StringField('What is your name?', validators=[Required()])
	submit = SubmitField('Submit')

#Flask类构造函数需要自己的名字作为参数
#app是Flask实例，是Flask的对象
app=Flask(__name__)
app.config.from_pyfile('yourconfig.py', silent=True)
db= SQLAlchemy(app)

class Role(db.Model):
	__tablename__ = 'roles'
	id = db.Column(db.Integer, primary_key=True)
	name = db.Column(db.String(64), unique=True)
	users = db.relationship('User', backref='role', lazy='dynamic')  #?

	def __repr__(self):
		return '<Role %r>' % self.name

class User(db.Model):
	"""docstring for User"""
	__tablename__ = 'users'
	id = db.Column(db.Integer, primary_key=True)
	username = db.Column(db.String(64), unique=True, index=True)
	role_id = db.Column(db.Integer, db.ForeignKey('roles.id'))
	
	def __repr__(self):
		return '<User %r>' % self.name
		


@app.route('/user/',methods=['GET','POST'])
def user():
	name=None
	form = NameForm()
	if form.validate_on_submit():
		user = User.query.filter_by(username=form.name.data).first()
		if user is None:
			user = User(username=form.name.data)
			db.session.add(user)
			session['known']=False
		else:
			session['known']=True		
		session['name'] = form.name.data
		form.name.date='' #清空表单中name
		return redirect(url_for('user'))
	return render_template('user.html',form=form,name=session.get('name'),
		known=session.get('known',False))

@app.errorhandler(404)
def page_not_found(e):
	return render_template('404.html'), 404

@app.errorhandler(500)
def page_not_found(e):
	return render_template('500.html'), 500

@app.route('/')
def index():
	return render_template('index.html', current_time=datetime.utcnow())

def make_shell_context():
	return dict(app=app, db=db, User=User, Role=Role)

def send_email(to, subject, template, **kwargs):
	msg=Message(app.config['FLASKY_MAIL_SUBJECT_PREFIX'] + subject,
		sender=app.config['FLASKY_MAIL_SENDER'],recipients=[to])
	msg.body = render_template(template + '.txt',**kwargs)
	msg.html = render_template(template + '.html',**kwargs)
	mail.send(msg)

manager = Manager(app)
manager.add_command("shell", Shell(make_context=make_shell_context))
migrate = Migrate(app, db)
manager.add_command('db', MigrateCommand)

mail=Mail(app)
#程序实例作为参数传递给构造函数，初始化主类的实例，得到一个扩展类的对象
bootstrap = Bootstrap(app)
moment = Moment(app)
if __name__ == '__main__':
	manager.run()

#上下文推送
#app_ctx=app.app_context()
#app_ctx.push()
#print current_app.name