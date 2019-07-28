from flask import url_for
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField, IntegerField, HiddenField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
from ahmaths.models import User, Question


class SignupForm(FlaskForm):
    username = StringField('Username',
                            validators=[DataRequired(), Length(min=2, max=20)])

    email = StringField('Email',
                        validators=[DataRequired(), Email()])

    password = PasswordField('Password',
                            validators=[DataRequired()])

    confirm_password = PasswordField('Confirm Password',
                                    validators=[DataRequired(), EqualTo('password')])

    submit = SubmitField('Sign Up')

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data.lower()).first()
        if user:
            raise ValidationError('That username is taken. Please choose a different one.')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError(f'An account with that email address already exists. If you already have an account please <a href="{url_for("login")}">log in</a>.')


class LoginForm(FlaskForm):
    username = StringField('Username',
                        validators=[DataRequired()])

    password = PasswordField('Password',
                            validators=[DataRequired()])

    remember = BooleanField('Remember me')

    submit = SubmitField('Log in')

class MarkForm(FlaskForm):
    question = HiddenField('Question')
    mark = IntegerField('Mark',
                        validators=[DataRequired()])
    submit = SubmitField('Submit')
    def validate_mark(self, mark):
        question = self.question
        mark = int(mark.data)
        max_mark = int(Question.query.filter_by(question_id=question.data).first().marks)
        if mark > max_mark or mark < 0:
            raise ValidationError('Mark must be between 0 and ' + str(max_mark) + '.')
