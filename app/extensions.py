# Flask limiter
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address

limiter = Limiter(key_func=get_remote_address)

# Flask security
from flask_security import Security

security = Security()

# Flask session
from flask_session import Session
session = Session()

# SQLAlchemy
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

# Flask login
from flask import current_app
from flask_login import LoginManager
from app.models.users import User

login_manager = LoginManager()

@login_manager.user_loader
def load_user(user_id):
    """Loads a user from the current Flask app.

    Attributes:
        user_id: Username.

    Returns:
        A user or None.
    """
    blueprint = current_app.blueprints[request.blueprint]

    return User.query.get(int(user_id))
