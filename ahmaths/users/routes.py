from flask import render_template, url_for, redirect, flash, request, Blueprint, current_app
from flask_login import login_user, logout_user, current_user, login_required
from ahmaths import bcrypt, db
from ahmaths.models import User
from ahmaths.users.forms import SignupForm, LoginForm, RequestResetPasswordForm, ResetPasswordForm
from ahmaths.users.utils import send_reset_password_email

users = Blueprint('users', __name__)


@users.route('/signup', methods=['GET', 'POST'])
def signup():
    if current_user.is_authenticated:
        return render_template('main/home.html.j2')
    form = SignupForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(email=form.email.data, password=hashed_password)
        db.session.add(user)
        db.session.commit()
        login_user(user)
        return redirect(url_for('main.home'))
    form.validate_on_submit()
    return render_template('users/signup.html.j2', form=form, title='Sign Up')


@users.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return render_template('main/home.html.j2')
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data.lower()).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('main.home'))
        else:
            flash('Login unsuccessful. Please check your email address and password.', 'danger')
    return render_template('users/login.html.j2', form=form, title='Login')


@users.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('main.index'))


@users.route('/account')
@login_required
def account():
    return render_template('users/account.html.j2')


@users.route('/reset_password', methods=['GET', 'POST'])
def request_reset_password():
    if current_user.is_authenticated:
        return render_template('main/home.html.j2')
    form = RequestResetPasswordForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        send_reset_password_email(user)
        flash('Instructions to reset your password have been sent to your email address. If you have not received an email within 5 minutes, please check your spam folder or try requesting a password reset again.', 'info')
        return redirect(url_for('users.login'))
    return render_template('users/request_reset_password.html.j2', title='Reset Password', form=form)


@users.route('/reset_password/<string:token>', methods=['GET', 'POST'])
def reset_password(token):
    if current_user.is_authenticated:
        return render_template('main/home.html.j2')
    user = User.verify_reset_token(token)
    if user is None:
        flash('Invalid or expired password reset link. Please request another password reset link.', 'warning')
        return redirect(url_for('users.request_reset_password'))
    form = ResetPasswordForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user.password = hashed_password
        db.session.commit()
        flash('Your password has been reset. You may now use your new password to log in to your account.', 'info')
        return redirect(url_for('users.login'))
    return render_template('users/reset_password.html.j2', title='Reset Password', form=form)
