from flask import render_template, request, current_app, make_response, redirect
from flask_login import login_required, current_user
from wtforms.fields.core import UnboundField
from . import blueprint
from .utils import list_deployed_vms, get_vm_details
from constants import NTNX_COOKIE


@blueprint.route('/')
@login_required
def index():
    deployed_vms = list_deployed_vms(current_user)
    return render_template('vms/index.html', segment=['vms'], vms=deployed_vms)


@blueprint.route('/details', methods=['GET'])
@login_required
def details():
    vmuuid = request.args.get('vm_uuid')
    vm_details = get_vm_details(vmuuid, current_user)
    #return str(vm_details)
    return render_template('vms/details.html', segment=['vms'], vm_details=vm_details, vm_uuid=vmuuid)


@blueprint.route('/console/<vm_uuid>', methods=['GET'])
@login_required
def console(vm_uuid):
    vm_details = get_vm_details(vm_uuid, current_user)
    cluster_uuid = vm_details['cluster_reference']['uuid']
    console_url = f'/console/lib/noVNC/vnc_auto.html?path=vnc/vm/{vm_uuid}/proxy' \
                  f'&uuid={vm_uuid}&title={vm_uuid}&attached=true&hypervisorType=kKvm' \
                  f'&controllerVm=false&vmName={vm_uuid}&noV1Access=true&useV3=true' \
                  f'&isXi=false&clusterId={cluster_uuid}'
    resp = make_response(redirect(console_url))
    resp.set_cookie(NTNX_COOKIE, current_user.cookie, current_user.expiry_timedelta)
    return resp
    