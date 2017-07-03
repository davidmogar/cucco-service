from flask_security import RoleMixin

from app.extensions import db

class Role(db.Model, RoleMixin):
    __tablename__ = 'roles'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=True)
    description = db.Column(db.String(255))

    def __init__(self, name, description):
        assert name != '' or name is not None

        self.name = name
        self.description = description if description else ''

    def __repr__(self):
        return self.name
