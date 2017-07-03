from flask import Blueprint, flash, make_response, jsonify, redirect, render_template, request, url_for
from flask_login import login_required, logout_user, current_user, login_user
from flask_security import current_user
from flask_security.utils import encrypt_password, verify_password

from app.forms.users import ChangePasswordForm, LoginForm, SignUpForm
from app.models import user_datastore
from app.models.users import User

users = Blueprint('users', __name__)


@users.route("/generate")
@login_required
def generate():
    current_user.api_key = User.generate_key()
    user_datastore.commit()

    flash('Your API credentials have been updated', 'info')

    return redirect(url_for("users.profile"))

@users.route('/login', methods=['GET', 'POST'])
def login():
    login_form = LoginForm()
    signup_form = SignUpForm()

    if login_form.login.data:
        if process_login_request(login_form):
            return redirect(url_for('users.profile'))
    elif signup_form.signup.data:
        if process_signup_request(signup_form):
            return redirect(url_for('users.profile'))

    return render_template('users/login.html',
                           login_form=login_form,
                           signup_form=signup_form)

@users.route("/logout")
@login_required
def logout():
    logout_user()

    flash("You have logged out")

    return redirect(url_for("users.login"))

@users.route('/', methods=['GET', 'POST'])
@users.route('/profile', methods=['GET', 'POST'])
@login_required
def profile():
    form = ChangePasswordForm()

    if request.method == 'POST':
        if form.validate_on_submit():
            current_user.password = encrypt_password(form.password.data)
            user_datastore.commit()
            flash('Your password has been updated')

    template = None
    if current_user.has_role('admin'):
        users = User.query.order_by(User.username)
        template = render_template('users/profile.html', form=form, users=users)
    else:
        template = render_template('users/profile.html', form=form)

    return template

@users.route('/users/<user_id>/remove', methods=['GET'])
def remove(user_id):
    removed = False
    user = user_datastore.find_user(id=user_id)
    if user:
        user_datastore.delete_user(user)
        user_datastore.commit()
        removed = True

    return make_response(jsonify(removed=True, user_id=user_id))

def process_login_request(form):
    valid = False

    if form.validate_on_submit():
        print('valid form')
        user = user_datastore.get_user(form.email.data)
        if user:
            print('found user')
            if verify_password(form.password.data, user.password):
                print('valid password')
                if login_user(user):
                    print('login')
                    user.authenticated = True
                    user_datastore.commit()
                    valid = True

    if not valid:
        flash('Invalid credentials', 'error')

    return valid

def process_signup_request(form):
    valid = False

    if form.validate_on_submit():
        user = user_datastore.create_user(username=form.username.data,
                                          email=form.email.data,
                                          password=encrypt_password(form.password.data))
        user_datastore.add_role_to_user(user, 'user')
        user_datastore.commit()
        if login_user(user):
            user_datastore.commit()
            valid = True

    return valid
