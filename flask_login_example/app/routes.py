from flask import Blueprint, flash, redirect, render_template, url_for
from flask.json import dumps
from flask_login import current_user, login_required, login_user, logout_user
from sqlalchemy import desc, func

from app import db
from app.forms import LoginForm, RegistrationForm
from app.models import User

login_bp = Blueprint('login_bp', __name__)

@login_bp.route('/', methods=['GET', 'POST'])
def login_page():
    # if user is already logged in then redirect to index page...
    if current_user.is_authenticated:
        return redirect(url_for('login_bp.index'))

    # if a login request is received...
    login_form = LoginForm()
    if login_form.validate_on_submit():
        user = User.query.filter_by(username=login_form.LoginUsername.data).first()
        if user is None or not user.check_password(login_form.LoginPassword.data):
            flash('Username not recognised or invalid password provided - please try again')
            return redirect(url_for('login_bp.login_page'))
        else:
            login_user(user)
            return redirect(url_for('login_bp.index'))

    # if a registration request is received...
    registration_form = RegistrationForm()
    if registration_form.is_submitted():
        if registration_form.validate():
            user = User(username=registration_form.RegistrationUsername.data,
                        identity=registration_form.Identity.data,
                        alignment=registration_form.Alignment.data,
                        gender=registration_form.Gender.data,
                        sex=registration_form.Sex.data,
                        eye_colour=registration_form.EyeColour.data,
                        hair_colour=registration_form.HairColour.data,
                        is_alive={'living': True, 'deceased': False}[registration_form.Alive.data],
                        appearances=registration_form.Appearances.data)
            user.set_password(registration_form.RegistrationPassword.data)
            db.session.add(user)
            db.session.commit()
            login_user(user)
            return redirect(url_for('login_bp.index'))
        else:
            return render_template('login.html', login_form=login_form, registration_form=registration_form, registration_active=True), 205

    # else we have landed on the login page via a GET request...
    return render_template('login.html', login_form=login_form, registration_form=registration_form, registration_active=False)


@login_bp.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('login_bp.login_page'))


@login_bp.route('/index')
@login_required
def index():
    eye_data, hair_data = get_statistics()
    return render_template('index.html', eye_data=dumps(eye_data), hair_data=dumps(hair_data))


def get_statistics():
    eye_data = db.session \
                 .query(User.eye_colour, func.count(User.eye_colour)) \
                 .group_by(User.eye_colour) \
                 .order_by(desc(func.count(User.eye_colour))) \
                 .all()
    if len(eye_data) >= 8:
        others = ('Other', sum(d[1] for d in eye_data[7:]))
        eye_data = eye_data[:8] + [others]
    hair_data = db.session \
                  .query(User.hair_colour, func.count(User.hair_colour)) \
                  .group_by(User.hair_colour) \
                  .order_by(desc(func.count(User.hair_colour))) \
                  .all()
    if len(hair_data) >= 8:
        others = ('Other', sum(d[1] for d in hair_data[7:]))
        hair_data = hair_data[:8] + [others]
    return eye_data, hair_data
