import urllib3
from flask import Flask, render_template
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy
from importlib import import_module


db = SQLAlchemy()
login_manager = LoginManager()


def register_extensions(app):
    db.init_app(app)
    login_manager.init_app(app)
    login_manager.login_view = 'auth.login'


def configure_database(app):

    @app.before_first_request
    def initialize_database():
        db.create_all()

    @app.teardown_request
    def shutdown_session(exception=None):
        db.session.remove()


def register_custom_error(app):

    @app.errorhandler(403)
    def page_authorization_error(e):
        return render_template('error/page-403.html'), 403

    @app.errorhandler(404)
    def page_not_found(e):
        return render_template('error/page-404.html'), 404

    @app.errorhandler(500)
    def page_internal_error(e):
        return render_template('error/page-500.html'), 500


def register_blueprints(app):
    for module_name in ('auth', 'dashboard', 'vms', 'marketplace'):
        module = import_module(f'app.{module_name}')
        app.register_blueprint(module.blueprint)


def create_app(config):
    app = Flask(__name__)
    app.config.from_object(config)

    register_extensions(app)
    configure_database(app)
    register_custom_error(app)
    register_blueprints(app)

    # disable ssl warning if SSL_VERIFY is disabled
    if not app.config['SSL_VERIFY']:
        urllib3.disable_warnings()

    return app
