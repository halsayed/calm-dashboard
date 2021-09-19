from flask import render_template, flash, current_app, redirect, url_for
from flask_login import current_user

from . import blueprint
from .forms import LoginForm
from .utils import authenticate, update_user_authentication, delete_user
from .models import User


@blueprint.route('/')
def default():
    return redirect(url_for('auth.login'))


@blueprint.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()

    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data
        auth_result = authenticate(username, password)
        if auth_result:
            user = update_user_authentication(**auth_result)
            current_app.logger.info(f'{username} authenticated successfully')
            current_app.logger.debug(user)
            return redirect(url_for('dashboard.index'))
        else:
            current_app.logger.info(f'{username} authentication failed!')
            flash('Sorry, authentication failed', 'danger')

    if current_user.is_authenticated:
        return redirect(url_for('dashboard.index'))

    return render_template('auth/login.html', form=form, html_title='Login')


@blueprint.route('/logout')
def logout():
    if current_user.is_authenticated:
        delete_user(current_user)

    return redirect(url_for('dashboard.index'))
