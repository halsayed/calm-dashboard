from flask import render_template, request
from flask_login import login_required, current_user
from . import blueprint
from .utils import list_deployed_apps, list_marketplace_items


@blueprint.route('/')
@login_required
def index():
    deployed_apps = list_deployed_apps(current_user)
    return render_template('dashboard/index.html', segment=['dashboard'], apps=deployed_apps)

@blueprint.route('/taskselect/<task>', methods= ['GET', 'POST'])
@login_required
def taskselect(task):
    if request.method == 'GET':
        available_items = list_marketplace_items(current_user)
        return str(available_items)
        #return render_template('taskvm/index.html', segment=['virtual_machines'], marketplace_items=available_items)
    if request.method == 'POST':
        return '''abc'''