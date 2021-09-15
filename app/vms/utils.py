from datetime import datetime

from werkzeug.wrappers.request import StreamOnlyMixin
from app.auth.models import User


def list_deployed_vms(user: User) -> list:
    """
    Returns a list of deployed application
    :param user:
    :return:
    """
    payload = {
        'kind': 'vm',
        'filter': ''
    }
    r = user.api_post('vms/list', payload)
    vms = []
    if r.status_code == 200:
        for vm in r.json()['entities']:
            vms.append({
                'memory': vm['spec']['resources']['memory_size_mib'],
                'name': vm['spec']['name'],
                'power_state': vm['spec']['resources']['power_state'],
                'vm_uuid': vm['metadata']['uuid'],
                'cluster_uuid': vm['spec']['cluster_reference']['uuid']
            })

    return vms

def get_vm_details(uuid, user: User) -> list:
    """
    Returns Details of a VM
    :param uuid, user:
    :return:
    """

    r = user.api_get('vms/'+uuid)
    if r.status_code == 200:
        vm_details =r.json()['status']
        
    return vm_details

