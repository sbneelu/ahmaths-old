from flask import render_template, url_for, redirect, Blueprint
from flask_login import current_user

main = Blueprint('main', __name__)


@main.route('/')
def index():
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))
    return render_template('index.html.j2')


@main.route('/home')
def home():
    if current_user.is_authenticated:
        return render_template('main/home.html.j2')
    return redirect(url_for('main.index'))
