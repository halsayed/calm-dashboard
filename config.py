import os
from decouple import config
from constants import API_BASE
from urllib.parse import urljoin


class Config(object):

    basedir = os.path.abspath(os.path.dirname(__file__))
    SECRET_KEY = config('SECRET_KEY', default='S#perS3crEt_123')
    PRISM_HOST = config('PRISM_HOST', default='127.0.0.1')
    PRISM_PORT = config('PRISM_PORT', default=9440, cast=int)
    SSL_VERIFY = config('SSL_VERIFY', default=False, cast=bool)
    API_BASE = urljoin(f'https://{PRISM_HOST}:{PRISM_PORT}', API_BASE)

    SQLALCHEMY_DATABASE_URI = 'sqlite:///:memory:'
    # SQLALCHEMY_DATABASE_URI = 'sqlite:///sql.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False


class ProductionConfig(Config):
    DEBUG = False


class DebugConfig(Config):
    DEBUG = True


config_dict = {
    'Production': ProductionConfig,
    'Debug': DebugConfig
}
