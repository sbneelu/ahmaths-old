from flask import url_for
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField
from wtforms.validators import DataRequired, Email, ValidationError, EqualTo, Length
from ahmaths.models import User


class SignupForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired(), Length(min=8, message='Password must be at least 8 characters long.')])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password', message='Password and Confirm Password must be identical. Note that passwords are case-sensitive.')])
    beta_token = StringField('Beta Access Token', validators=[DataRequired()])
    submit = SubmitField('Sign Up')

    def validate_beta_token(self, beta_token):
        if self.beta_token.data.strip() != 'Fb3tMg':
            raise ValidationError('Invalid beta access token.')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError(f'An account with that email address already exists. If you already have an account please <a href="{url_for("users.login")}">log in</a>.')


class LoginForm(FlaskForm):
    email = StringField('Email address', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember = BooleanField('Remember me')
    submit = SubmitField('Log in')


class RequestResetPasswordForm(FlaskForm):
    email = StringField('Email address', validators=[DataRequired(), Email()])
    submit = SubmitField('Request Password Reset')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user is None:
            raise ValidationError(f'There is no account with that email address. If you do not have an account then please <a href="' + url_for('users.signup') + '">sign up</a>.')


class ResetPasswordForm(FlaskForm):
    password = PasswordField('Password', validators=[DataRequired(), Length(min=8, message='Password must be at least 8 characters long.')])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password', message='Password and Confirm Password must be identical. Note that passwords are case-sensitive.')])
    submit = SubmitField('Update Password')
