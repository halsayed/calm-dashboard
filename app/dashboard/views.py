from flask import render_template, request, current_app
from flask_login import login_required, current_user
from werkzeug.utils import redirect
from . import blueprint
from .utils import list_deployed_apps, project_meter


@blueprint.route('/')
@login_required
def index():
    current_app.logger.debug('Entering dashboard.index view')
    deployed_apps = list_deployed_apps(current_user)
    usage = project_meter (current_user)
    current_app.logger.debug('Returning dashboard.index Template')
    return render_template('dashboard/index.html', segment=['dashboard'], apps=deployed_apps, usage=usage)

@blueprint.route('/taskselect/<task>', methods= ['GET'])
@login_required
def taskselect(task):
    if task == 'vm':
        return redirect('/marketplace')