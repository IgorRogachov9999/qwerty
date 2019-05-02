from app import db
from app.models import User, Message
from flask_login import current_user


def includes(users, user_id):
    for user in users:
        if user.id == user_id:
            return True
    return False


def get_new_count(username1, username2):
    chat = get_chat(username1, username2)
    count = 0
    for message in chat:
        if message.users[1].username == username1 and not message.is_read:
            count += 1
    return count


def get_chat_users(username):
    all_messages = Message.query.order_by(Message.send_time.desc())
    chat_users = []
    for message in all_messages:
        users = message.users
        user = None
        if users[0].username == username:
            user = users[1]
        elif users[1].username == username:
            user = users[0]
        
        if user is not None and not includes(chat_users, user.id):
            chat_users.append(user)
    return chat_users


def get_chat(username1, username2):
    all_messages = Message.query.order_by(Message.send_time.desc())
    chat = []
    for message in all_messages:
        user0 = message.users[0].username
        user1 = message.users[1].username
        if (user0 == username1 or user0 == username2) and \
                (user1 == username1 or user1 == username2):
            chat.append(message)
    return chat


def find_users(username):
    all_users = User.query.all()
    users = []
    for user in all_users:
        if username in user.username:
            users.append(user)
    return users