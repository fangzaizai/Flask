# -*- coding:utf-8 -*-
from datetime import datetime
from flask import Flask,render_template,session,redirect,url_for,flash
from . import main
from .forms import NameForm
from .. import db
from ..models import User

@main.route('/',methods=['GET','POST'])
def index():
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
		return redirect(url_for('.index'))
	return render_template('index.html',form=form,name=session.get('name'),
		known=session.get('known',False))

@main.route('/time')
def index1():
	return render_template('index_time.html', current_time=datetime.utcnow())