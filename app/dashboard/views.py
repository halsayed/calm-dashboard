from flask import render_template
from flask_login import login_required, current_user
from . import blueprint
from .utils import list_deployed_apps


@blueprint.route('/')
@login_required
def index():
    deployed_apps = list_deployed_apps(current_user)
    return render_template('dashboard/index.html', segment=['dashboard'], apps=deployed_apps)