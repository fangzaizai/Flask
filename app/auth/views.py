# -*- coding:utf-8 -*-
from flask import render_template, redirect, request, url_for, flash
from . import auth
from flask_login import login_user,logout_user, login_required, current_user
import flask_login.utils
from ..models import User
from .forms import LoginForm, RegistrationForm
from app import db
from ..email import send_email

@auth.before_app_request
def before_request():
	if current_user.is_authenticated \
			and not current_user.confirmed \
			and request.endpoint[:5] != 'auth.' \
			and request.endpoint != 'static':
		return redirect(url_for('auth.unconfirmed'))

@auth.route('/unconfirmed')
def unconfirmed():
	if current_user.ia_anonymous() or current_user.confirmed:
		return redirect(url_for('main.index'))
	return render_template('auth/unconfirmed.html')


@auth.route('/login', methods=['GET', 'POST'])
def login():
	form = LoginForm()
	if form.validate_on_submit():
		user = User.query.filter_by(email=form.email.data).first()
		if user is not None and user.verify_password(form.password.data):
			login_user(user, form.remember_me.data)
			#把原地址保存在查询字符串的next参数中
			return redirect(request.args.get('next') or url_for('main.index'))
		flash('Invalid username or password')
	return render_template('auth/login.html', form=form)

@auth.route('/logout')
@login_required
def logout():
	logout_user()
	flash('You have been logged out.')
	return redirect(url_for('main.index'))

@auth.route('/register', methods=['GET', 'POST'])
def register():
	form = RegistrationForm()
	#验证通过
	if form.validate_on_submit():
		user = User(email=form.email.data,
					username=form.username.data,
					password=form.password.data)
		db.session.add(user)
		db.session.commit()
		token = user.generate_confirmation_token()
		send_email(user.email,"Confirm Your Account",'auth/email/confirm',user=user, token=token)
		flash('confirm mail has sent')
		return redirect(url_for('main.index'))
	return render_template('auth/register.html', form=form)

@auth.route('/confirm/<token>')
@login_required
def confirm(token):  #is it the confirm in User?
	if current_user.confirmed:#调用了
		return redirect(url_for('main.index'))
	if current_user.confirm(token):
		flash('You have confirmed your account, thanks')
	else:
		flash('The confirmation link is invalid')
	return redirect(url_for('main.index'))

@auth.route('/confirm')
@login_required
def resend_confirmation():
	token=current_user.generate_confirmation_token()
	send_email(current_user.eamil, 'Confirm your Account','auth/email/confirm',user=current_user, token=token)
	flash('A new email has sent')
	return redirect(url_for('main.index'))