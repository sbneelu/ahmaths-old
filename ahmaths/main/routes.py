from flask import render_template, url_for, redirect, flash, Blueprint
from flask_login import current_user
from ahmaths.main.forms import ContactForm
from ahmaths.main.utils import send_contact_email

main = Blueprint('main', __name__)


@main.route('/')
def index():
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))
    return render_template('main/index.html.j2')


@main.route('/home')
def home():
    if current_user.is_authenticated:
        return render_template('main/home.html.j2')
    return redirect(url_for('main.index'))


@main.route('/contact', methods=['GET', 'POST'])
def contact():
    form = ContactForm()
    if form.validate_on_submit():
        send_contact_email(form.name.data, form.email.data, form.subject.data, form.message.data)
        flash('Your message has been sent. If you do not hear back within 24 hours then please send an email to <a href="mailto:neelu.rsa@gmail.com">neelu.rsa@gmail.com</a>.', 'info')
        return redirect(url_for('main.home'))
    return render_template('main/contact.html.j2', title="Contact/Report a Problem", form=form)
