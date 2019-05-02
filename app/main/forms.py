from flask import request
from flask_login import current_user
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, TextAreaField, PasswordField
from wtforms.validators import ValidationError, Length, ValidationError, \
                               DataRequired, Email, EqualTo
from app.models import User, Message


class EditProfileForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    language = StringField('Language', validators=[DataRequired()])
    submit = SubmitField(('Edit'))


    def __init__(self, original_username, *args, **kwargs):
        super(EditProfileForm, self).__init__(*args, **kwargs)
        self.original_username = original_username


    def validate_username(self, username):
        if username.data != self.original_username:
            user = User.query.filter_by(username=self.username.data).first()
            if user is not None: 
                raise ValidationError('Please, use a different username.')


class ChangePasswordForm(FlaskForm):
    password_old = PasswordField('Old password',
                                  validators=[DataRequired()])
    password = PasswordField(('New Password'), validators=[DataRequired()])
    password2 = PasswordField(('Repeat New Password'),
                                validators=[DataRequired(),
                                            EqualTo('password')])
    submit = SubmitField('Register')

    def validate_password_old(form, field):
        if not current_user.check_password(field.data):
            raise ValidationError('Wrong old password')


class FindUserForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    submit = SubmitField('Find')


class SendMessageForm(FlaskForm):
    message = TextAreaField('Message', validators=[DataRequired()])
    submit = SubmitField('Send')
