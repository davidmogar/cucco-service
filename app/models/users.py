import uuid

from flask_security import UserMixin

from app.extensions import db


roles_users = db.Table('roles_users',
        db.Column('user_id', db.Integer(), db.ForeignKey('users.id')),
        db.Column('role_id', db.Integer(), db.ForeignKey('roles.id')))

class User(db.Model, UserMixin):
    """This class represents a user of the API.

    Attributes:
        username: Username of the user.
        email: Email address.
        password: Password of the user.
    """

    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), nullable=False)
    password = db.Column(db.String(255), nullable=False)
    email = db.Column(db.String, nullable=False, unique=True)
    created_at = db.Column(db.DateTime, default=db.func.current_timestamp())
    active = db.Column(db.Boolean(), default=True)
    api_key = db.Column(db.String(255), nullable=False)

    roles = db.relationship('Role', secondary=roles_users, backref=db.backref('users', lazy='dynamic'))


    def __init__(self, username, email, password, **kwargs):
        self.username = username
        self.email = email
        self.password = password
        self.active = True
        self.api_key = User.generate_key()

    def __repr__(self):
        return '<User({}, {}, username={}): {}>'.format(self.id, self.username, self.email, self.is_authenticated)

    @staticmethod
    def generate_key():
        """Generate an API key.

        Returns:
            A string representing a valid API key.
        """
        return uuid.uuid4().hex
