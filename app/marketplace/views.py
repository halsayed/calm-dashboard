from flask import render_template, request
from flask_login import login_required, current_user
from werkzeug.utils import redirect
from wtforms.fields.core import UnboundField
from . import blueprint
from .utils import launch_mpi, list_marketplace_items, get_runtime_editables
from flask import current_app

@blueprint.route('/')
@login_required
def index():
    available_items = list_marketplace_items(current_user)
    return render_template('marketplace/index.html', segment=['virtual_machines'], mpi_list=available_items)

@blueprint.route('/deploy', methods= ['GET','POST'])
@login_required
def deploy():
    if request.method == "POST":
        app_name = request.form['mpi_app_name']
        f = request.form
        runtime_editables=[]
        for key in f.keys():
            if key != 'mpi_app_name':
                for value in f.getlist(key):
                    current_app.logger.debug('Filling runtime_editables {0}:{1}'.format(key,value))
                    runtime_editables.append({
                        key: value
                    })
        mpi_uuid = request.args.get('mpi_uuid')
        pending_launch = launch_mpi(mpi_uuid, app_name, runtime_editables,current_user)
        return redirect('/')

    mpi_uuid = request.args.get('mpi_uuid')
    runtime_editables = get_runtime_editables(mpi_uuid, current_user)
    return render_template('marketplace/deploy.html', segment=['virtual_machines'], runtime_editables=runtime_editables)
