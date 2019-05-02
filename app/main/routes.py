from datetime import datetime
from flask import render_template, flash, redirect, url_for, request, \
    jsonify, current_app
from flask_login import current_user, login_required
from app import db
from app.main.forms import EditProfileForm, ChangePasswordForm, \
                           FindUserForm, SendMessageForm
from app.models import User, Message
from app.translate import translate
from app.main import bp
from app.queryes import get_chat_users, get_chat, find_users, get_new_count


@bp.before_app_request
def before_request():
    if current_user.is_authenticated:
        current_user.last_seen = datetime.utcnow()
        db.session.commit()


@bp.route('/')
@bp.route('/index')
@login_required
def index():
    chat_users = get_chat_users(current_user.username)
    return render_template('index.html', title='Chats',
                           chat_users=chat_users, 
                           get_new_count=get_new_count)


@bp.route('/chat/<currentusername>/<username>', methods=['GET', 'POST'])
@login_required
def chat(currentusername, username):
    form = SendMessageForm()
    messages = get_chat(currentusername, username)
    for message in messages:
        if message.users[1] == current_user:
            message.is_read = True
    if request.method == 'GET':
        db.session.commit()
    if form.validate_on_submit():
        body = form.message.data
        u1 = User.query.filter_by(username=currentusername).first()
        u2 = User.query.filter_by(username=username).first()
        message = Message(body=body)
        message.users.append(u1)
        message.users.append(u2)
        db.session.add(message)
        db.session.commit()
        messages.insert(0, message)
        redirect(url_for('main.chat', currentusername=currentusername, 
                         username=username))
    return render_template('chat.html', title='Chat', messages=messages,
                           form=form)


@bp.route('/profile/<username>')
@login_required
def profile(username):
    user = User.query.filter_by(username=username).first_or_404()
    return render_template('profile.html', user=user)


@bp.route('/edit_password', methods=['GET', 'POST'])
@login_required
def change_password():
    form = ChangePasswordForm()
    if form.validate_on_submit():
        password_old = form.password_old.data
        password = form.password.data
        password2 = form.password2.data
        current_user.set_password(password)
        db.session.commit()
        flash('Your changes have been saved.')
        return redirect(url_for('main.change_password'))
    return render_template('change_profile.html', title='Change Password',
                            form=form, label='Change Password')


@bp.route('/edit_profile', methods=['GET', 'POST'])
@login_required
def change_profile():
    form = EditProfileForm(current_user.username)
    if form.validate_on_submit():
        current_user.username = form.username.data
        current_user.email = form.email.data
        current_user.language = form.language.data
        db.session.commit()
        flash('Your changes have been saved.')
        return redirect(url_for('main.change_profile'))
    elif request.method == 'GET':
        form.username.data = current_user.username
        form.email.data = current_user.email 
        form.language.data = current_user.language
    return render_template('change_profile.html', title='Edit Profile',
                            form=form, label='Edit Profile')


@bp.route('/find', methods=['GET', 'POST'])
@login_required
def find():
    users = []
    form = FindUserForm()
    if form.validate_on_submit():
        username = form.username.data
        users = find_users(username)
    return render_template('find.html', title='Find User', 
                           users=users, form=form)


@bp.route('/translate', methods=['POST'])
@login_required
def translate_text():
    return jsonify({'text': translate(request.form['text'],
                                      request.form['dest_language'])})


