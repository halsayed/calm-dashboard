from flask import render_template, request
from flask_login import login_required, current_user
from werkzeug.utils import redirect
from . import blueprint
from .utils import list_deployed_apps


@blueprint.route('/')
@login_required
def index():
    deployed_apps = list_deployed_apps(current_user)
    return render_template('dashboard/index.html', segment=['dashboard'], apps=deployed_apps)

@blueprint.route('/taskselect/<task>', methods= ['GET'])
@login_required
def taskselect(task):
    if task == 'vm':
        return redirect('/marketplace')