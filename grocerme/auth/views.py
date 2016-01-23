from flask import render_template, redirect, request, url_for, flash
from flask.ext.login import login_user, logout_user, login_required
from . import auth_blueprint
from .forms import LoginForm, RegistrationForm
from ..users.models import User
from ..extensions import db
from ..utils.decorators import anonymous_user_required
from ..utils.helpers import redirect_url

@auth_blueprint.route('/login', methods=['GET', 'POST'])
@anonymous_user_required
def login():
    form = LoginForm()

    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()

        if user is not None and user.verify_password(form.password.data):
            login_user(user, form.remember_me.data)
            return redirect(url_for("main_blueprint.index"))

        flash('Invalid username or password')

    return render_template('auth/login.html', form=form)

@auth_blueprint.route('/register', methods=['GET', 'POST'])
@anonymous_user_required
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(email=form.email.data,
                    username=form.username.data,
                    password=form.password.data)
        user.save()
        flash('You can now login.')
        return redirect(url_for('auth_blueprint.login'))
    return render_template('auth/register.html', form = form)

@auth_blueprint.route('/logout')
def logout():
    logout_user()
    flash('You have been logged out')
    return redirect(url_for("main_blueprint.index"))