from flask_security import current_user
from flask_security.utils import verify_password
from flask_wtf import FlaskForm
from wtforms import TextField, PasswordField, ValidationError, StringField, SubmitField
from wtforms.validators import Required, Email, Length, Regexp, EqualTo, DataRequired
from app.models import user_datastore

class UniqueUser(object):
    """Validator to guarantee user uniqueness."""

    def __init__(self, message='User exists'):
        self.message = message

    def __call__(self, form, field):
        if user_datastore.find_user(email=field.data):
            raise ValidationError(self.message)

class ValidPassword(object):
    """Validator to guarantee password validity."""

    def __init__(self, message='Password invalid'):
        self.message = message

    def __call__(self, form, field):
        if not current_user or verify_password(current_user.password,
                                               field.data):
            raise ValidationError(self.message)

email_validator = [
    DataRequired(),
    Email(),
    UniqueUser(message='Email address is associated with '
                       'an existing account')
]

password_validator = [
    DataRequired(),
    Length(min=6, max=50),
    EqualTo('confirm', message='Passwords must match'),
    Regexp(r'[A-Za-z0-9@#$%^&+=]',
           message='Password contains invalid characters')
]

class ChangePasswordForm(FlaskForm):
    """This class represent a change password form."""

    password = PasswordField('Current password', [ DataRequired(), ValidPassword() ])
    new_password = PasswordField('Password', password_validator)
    confirm = PasswordField('Confirm Password')

class LoginForm(FlaskForm):
    """This class represent a login form."""

    email = StringField('Email', [ DataRequired(), Email() ])
    password = PasswordField('Password', [ DataRequired() ])
    login = SubmitField('Login')

class SignUpForm(FlaskForm):
    """This class represent a sign-up form."""

    username = StringField('Username', [
        DataRequired(),
        Length(min=3, max=20)
    ])
    email = StringField('Email', email_validator)
    password = PasswordField('Password', password_validator)
    confirm = PasswordField('Confirm Password')
    signup = SubmitField('Sign up')
