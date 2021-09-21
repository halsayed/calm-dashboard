import requests
from datetime import datetime
from flask import current_app
from flask_login import UserMixin
from urllib.parse import urljoin

from constants import NTNX_COOKIE
from app import db, login_manager
from .helpers import extract_cookie_details, expand_project_name, map_prism_role


class User(db.Model, UserMixin):
    __tablename__ = 'Users'

    uuid = db.Column(db.String(36), primary_key=True)
    username = db.Column(db.String(100), unique=True)
    expiry = db.Column(db.DATETIME)
    cookie = db.Column(db.String)
    name = db.Column(db.String)
    email = db.Column(db.String)
    mobile = db.Column(db.String)
    directory_uuid = db.Column(db.String(36))
    project = db.Column(db.String)
    project_code = db.Column(db.String)
    project_uuid = db.Column(db.String(36))
    is_admin = db.Column(db.Boolean, default=False)
    is_consumer = db.Column(db.Boolean, default=False)
    is_operator = db.Column(db.Boolean, default=True)

    def __init__(self, uuid: str, username: str, cookie: str, expiry: datetime):
        """

        :param uuid:
        :param username:
        :param cookie:
        :param expiry:
        """
        self.uuid = uuid
        self.username = username
        self.cookie = cookie
        self.expiry = expiry

        self._populate_user_info()

    def __repr__(self):
        return f'uuid:{self.uuid}, username: {self.username}, expiry: {self.expiry}, name: {self.name}, email: ' \
               f'{self.email}, project[name, code, uuid]: {self.project} {self.project_code} {self.project_uuid} ' \
               f'is_admin: {self.is_admin}, is_consumer: {self.is_consumer}, is_operator: {self.is_operator}'

    @property
    def is_authenticated(self):
        return datetime.now() < self.expiry

    @property
    def expiry_time(self):
        if (self.expiry - datetime.now()).total_seconds() > 0:
            return int((self.expiry - datetime.now()).total_seconds())

    @property
    def expiry_timedelta(self):
        return self.expiry - datetime.now()

    def get_id(self) -> str:
        return self.uuid

    def get_cookie(self) -> dict:
        return {NTNX_COOKIE: self.cookie}

    def _update_user_cookie(self, r: requests):
        self.cookie, self.expiry = extract_cookie_details(r.cookies)
        db.session.commit()

    def api_get(self, endpoint: str) -> requests:
        r = requests.get(urljoin(current_app.config['API_BASE'], endpoint),
                         cookies=self.get_cookie(),
                         verify=current_app.config['SSL_VERIFY'])
        self._update_user_cookie(r)
        return r

    def api_post(self, endpoint: str, payload: str) -> requests:
        r = requests.post(urljoin(current_app.config['API_BASE'], endpoint),
                          cookies=self.get_cookie(),
                          verify=current_app.config['SSL_VERIFY'],
                          json=payload)
        self._update_user_cookie(r)
        return r

    def _populate_user_info(self):
        r = self.api_get('users/me')

        if r.status_code != 200:
            current_app.logger.error(f'API call to obtain user info failed, status code: {r.status_code},'
                                     f'message: {r.content}')
            return

        resources = r.json()['status']['resources']

        self.name = resources.get('display_name')
        projects = resources.get('projects_reference_list', [])

        # check if the user is directory based or local
        if resources.get('directory_service_user'):
            self.directory_uuid = resources['directory_service_user']['directory_service_reference']['uuid']

        # remove default project from the list of usable projects
        projects = [project for project in projects if project['name'].lower() != 'default']

        # check if the user has any projects assigned other than default
        if len(projects):
            self.project_code, self.project = expand_project_name(projects[0]['name'])
            self.project_uuid = projects[0]['uuid']

        # check if the user has any roles and map Prism roles to (admin, superuser, viewer)
        # TODO: clean up this section or move it
        prism_role = None
        for acp in resources.get('access_control_policy_reference_list', []):
            r = self.api_get(f'access_control_policies/{acp["uuid"]}')
            for context in r.json()['status']['resources']['filter_list']['context_list']:
                for item in context.get('scope_filter_expression_list', []):
                    if item.get('left_hand_side') == 'PROJECT':
                        right_hand = item['right_hand_side']
                        if self.project_uuid in right_hand.get('uuid_list', []):
                            prism_role = r.json()['status']['resources']['role_reference']['name']
        self.is_admin, self.is_consumer, self.is_operator = map_prism_role(prism_role)

        # TODO: query AD using default consume role fails in PC, need a workaround
        # # get extra fields from directory service (email and mobile)
        # payload = {
        #     'query': self.username,
        #     'returned_attribute_list': ['mail', 'mobile'],
        #     'search_attribute_list': ['userPrincipalName'],
        #     'is_wildcard_search': False
        # }
        # r = self.api_post(f'directory_services/{self.directory_uuid}/search', payload)


@login_manager.user_loader
def user_loader(uuid):
    user = User.query.filter_by(uuid=uuid).first()
    if user and user.is_authenticated:
        return user

# @login_manager.request_loader
# def request_loader(request):
#     username = request.form.get('username')
#     user = User.query.filter_by(username=username).first()
#     return user if user else None
