import requests
from requests.auth import HTTPBasicAuth
from urllib.parse import urljoin
from flask import current_app
from flask_login import login_user, logout_user
from datetime import datetime

from app import db
from .models import User
from .helpers import extract_cookie_details


def authenticate(username: str, password: str) -> dict:
    """
    Authenticate user with Nutanix Prism
    :param username:
    :param password:
    :return: returns User object if login successful, and None if fail
    """
    # authenticate by using users/me endpoint to obtain user information
    r = requests.get(urljoin(current_app.config['API_BASE'], 'users/me'),
                     auth=HTTPBasicAuth(username, password),
                     verify=current_app.config['SSL_VERIFY'])

    # authentication passed, create user object
    if r.status_code == 200:
        user_json = r.json()
        user_id = user_json['metadata']['uuid']
        cookie_value, cookie_expiry = extract_cookie_details(r.cookies)

        user = {
            'uuid': user_id,
            'username': username,
            'expiry': cookie_expiry,
            'cookie': cookie_value
        }

        return user


def update_user_authentication(uuid: str, username: str, cookie: str, expiry: datetime) -> User:
    """
    Update User object with new authentication or create a new one if doesn't exists.
    :param uuid:
    :param username:
    :param cookie:
    :param expiry:
    :return:
    """

    # delete any previous expired session records
    users = User.query.filter_by(username=username)
    for user in users:
        if not user.is_authenticated:
            db.session.delete(user)

    user = User(uuid, username, cookie, expiry)
    current_app.logger.info(f'{username} not in temp db, adding user')
    login_user(user, duration=user.expiry_timedelta)
    db.session.add(user)

    db.session.commit()
    return user


def delete_user(user: User):
    """
    Logs out the user and delete the temp db record
    :param user:
    :return:
    """
    current_app.logger.info(f'logging out {user.username}')
    db.session.delete(user)
    db.session.commit()
    logout_user()

