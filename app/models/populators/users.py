from flask_security.utils import encrypt_password
from app.models import user_datastore
from app.models.users import User
from flask import current_app

def populate_users_table(app, db):
    """Populate users table.

    This method populate users table adding initial entries.

    Attributes:
        app: Instance of the Flask app.
        db: Instance of the database.
    """
    user_datastore
    with app.app_context():
        try:
            user = user_datastore.create_user(username='admin',
                                              email='admin@cucco.io',
                                              password=encrypt_password('admin'))
            user_datastore.add_role_to_user(user, 'admin')
            user_datastore.commit()
        except Exception as error:
            app.logger.debug("User already exists: %s" % error)
