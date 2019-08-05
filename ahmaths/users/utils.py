import os
from threading import Thread
from flask import url_for, current_app
from flask_mail import Message
from ahmaths import mail


def send_async_email(app, msg):
    with app.app_context():
        mail.send(msg)


def send_reset_password_email(user):
    token = user.get_reset_token()
    msg = Message('Reset your Password (AHMaths.com)', sender=os.environ.get('APP_TESTING_EMAIL'), recipients=[user.email])
    msg.body = f'''A password reset has been requested for your account. Please go to the following link to reset your password:
{url_for('users.reset_password', token=token, _external=True)}


If you did not request a password reset you do not need to do anything, and no changes will be made.'''
    Thread(target=send_async_email, args=(current_app, msg)).start()
