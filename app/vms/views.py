from flask import render_template, request
from flask_login import login_required, current_user
from wtforms.fields.core import UnboundField
from . import blueprint
from .utils import list_deployed_vms, get_vm_details


@blueprint.route('/')
@login_required
def index():
    deployed_vms = list_deployed_vms(current_user)
    return render_template('vms/index.html', segment=['vms'], vms=deployed_vms)

@blueprint.route('/details', methods=['GET'])
def console():
    vmuuid = request.args.get('vm_uuid')
    vm_details = get_vm_details(vmuuid, current_user)
    #return str(vm_details)
    return render_template('vms/details.html', segment=['vms'], vm_details=vm_details)
    