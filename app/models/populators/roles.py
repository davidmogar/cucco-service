from app.models.roles import Role
from flask import current_app

roles = [
    { 'name': 'admin', 'description': 'Application admins' },
    { 'name': 'user', 'description': 'Application users' }
]

def populate_roles_table(app, db):
    with app.app_context():
        for role_data in roles:
            try:
                role = Role(**role_data)

                db.session.add(role)
                db.session.commit()
            except Exception as error:
                app.logger.debug("Role already exists: %s" % error)
