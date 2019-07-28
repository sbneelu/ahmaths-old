from flask import render_template, url_for, redirect, flash, request
from ahmaths import app, bcrypt, db
from ahmaths.forms import SignupForm, LoginForm, MarkForm
from ahmaths.models import User, Topic, Question, Paper, Subtopic
from ahmaths.save_results import save_marks_to_topic, save_marks_to_progress
from flask_login import login_user, logout_user, current_user, login_required

@app.route('/')
def index():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    return render_template('index.html.j2')

@app.route('/home')
def home():
    if current_user.is_authenticated:
        return render_template('home.html.j2')
    return redirect(url_for('index'))

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    form = SignupForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(username=form.username.data.lower(), email=form.email.data, password=hashed_password)
        db.session.add(user)
        db.session.commit()
        login_user(user)
        return redirect(url_for('home'))
    form.validate_on_submit()
    return render_template('signup.html.j2', form=form, title='Sign Up')

@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data.lower()).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('home'))
        else:
            flash('Login unsuccessful. Please check your username and password.', 'danger')
    return render_template('login.html.j2', form=form, title='Login')

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))


@app.route('/practise')
@login_required
def practise():
    progress_strings = current_user.progress.split(',')
    progress = {}
    for progress_string in progress_strings:
        if progress_string != '':
            progress_string = progress_string.split(':')
            progress[progress_string[0]] = int(progress_string[1])
    return render_template('practise.html.j2', topics=Topic.query.all(), progress=progress, title='Practise')


@app.route('/practise/<string:topic_id>')
@login_required
def topic(topic_id):
    if Topic.query.filter_by(topic_id=topic_id).first():
        topic = Topic.query.filter_by(topic_id=topic_id).first()
        questions = Question.query.filter(Question.topics.contains(topic_id)).all()
        progress_strings = getattr(current_user, topic_id).split(',')
        # progress_strings = '2007Q4:0011,2011Q1:1111,2018Q2:0001'.split(',')
        progress = {}
        for progress_string in progress_strings:
            if progress_string != '':
                progress_string = progress_string.split(':')
                progress[progress_string[0]] = progress_string[1]
        return render_template('question-selection.html.j2', progress=progress, questions=reversed(questions), topic=topic, title=topic.topic_name + ' | Practise')
    else:
        flash('Invalid topic. Please try again.', 'danger')
        return redirect(url_for('practise'))


@app.route('/practise/question/<string:question_id>', methods=['GET', 'POST'])
@login_required
def question(question_id):
    if Question.query.filter_by(question_id=question_id).first():
        q = Question.query.filter_by(question_id=question_id).first()
        form = MarkForm()
        form.question.data = q.question_id
        form.mark.label.text += ' out of ' + str(q.marks)
        if form.validate_on_submit():
            topics = q.topics.split(',')
            for topic in topics:
                save_marks_to_topic(topic, question_id, form.mark.data)
                save_marks_to_progress(topic)
            flash('Your marks have been recorded.', 'success')
            return redirect(url_for('practise'))
        q = Question.query.filter_by(question_id=question_id).first()
        topics = []
        subtopics = {}
        for topic in q.topics.split(','):
            topics += [Topic.query.filter_by(topic_id=topic).first()]
            for subtopic in q.subtopics.split(','):
                if Subtopic.query.filter_by(subtopic_id = subtopic).first() and Subtopic.query.filter_by(subtopic_id = subtopic).first().topic_id == topic:
                    if topic not in subtopics:
                        subtopics[topic] = []
                    subtopics[topic] += [Subtopic.query.filter_by(subtopic_id = subtopic).first()]

        progress_strings = getattr(current_user, topic).split(',')
        progress = {}
        for progress_string in progress_strings:
            if progress_string != '':
                progress_string = progress_string.split(':')
                progress[progress_string[0]] = progress_string[1]
        mark = progress[question_id] if question_id in progress else None
        show_marking = request.args.get('show_marking')
        if show_marking == 'mark_validation_error':
            flash('Invalid mark. Please scroll down and try again. Please make sure the mark is a whole number between 0 and ' + str(q.marks) + '.', 'danger')
        return render_template('question.html.j2', show_marking=show_marking, question=q, topics=topics, subtopics=subtopics, mark=mark, form=form, title='Practise')
    else:
        flash('Invalid question. Please try again.', 'danger')
        return redirect(url_for('practise'))

@app.route('/revise')
def revise():
    papers = Paper.query.all()
    return render_template('revise.html.j2', papers=papers, title='Revise')

@app.route('/learn')
def learn():
    topics = Topic.query.all()
    return render_template('learn.html.j2', topics=topics, title='Learn')

@app.route('/learn/<string:topic_id>')
def learn_topic(topic_id):
    topic = Topic.query.filter_by(topic_id=topic_id).first()
    if topic:
        return render_template('learn-topics/' + topic.topic_id + '/topic.html.j2', topic=topic, title=topic.topic_name + ' | Learn')
    else:
        flash('Invalid topic. Please try again.', 'danger')
        return redirect(url_for('learn'))

@app.route('/learn/<string:topic_id>/<string:subtopic_id>')
def learn_subtopic(topic_id, subtopic_id):
    topic = Topic.query.filter_by(topic_id=topic_id).first()
    if topic:
        subtopic = Subtopic.query.filter_by(subtopic_id=subtopic_id).first()
        if subtopic and subtopic.topic.topic_id == topic_id:
            return render_template('learn-topics/' + topic.topic_id + '/' + subtopic.subtopic_id + '.html.j2', topic=topic, subtopic=subtopic, title=subtopic.subtopic_name + ' | Learn')
        else:
            flash('Invalid subtopic. Please try again.', 'danger')
            return redirect(url_for('learn_topic', topic_id=topic_id))
    else:
        flash('Invalid topic. Please try again.', 'danger')
        return redirect(url_for('learn'))

@app.route('/<path:path>/')
def trailing_slash_redirect(path):
    return redirect('/' + path)
