from flask_security import SQLAlchemyUserDatastore
from app.extensions import db

from app.models.roles import Role
from app.models.users import User

user_datastore = SQLAlchemyUserDatastore(db, User, Role)
