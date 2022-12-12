from datetime import datetime
from app.auth.models import User, user_loader
from flask import current_app


def list_deployed_apps(user: User) -> list:
    """
    Returns a list of deployed application
    :param user:
    :return:
    """
    payload = {
        'kind': 'app',
        'filter': ''
    }
    r = user.api_post('apps/list', payload)
    apps = []
    if r.status_code == 200:
        for app in r.json()['entities']:
            apps.append({
                'uuid': app['status']['uuid'],
                'name': app['status']['name'],
                'state': app['status']['state'],
                'creation_time': datetime.fromtimestamp(int(app['status']['creation_time'])/1000000)
            })

    return apps


def project_meter(user: User):
    """
    Returns project meter details
    :param user:
    :return:
    """
    current_app.logger.debug('project_meter: project_uuid={}'.format(user.project_uuid))
    payload = {
        'filter':'(project=={})'.format(user.project_uuid)
    }

    r = user.api_post('meter/projects/list', payload)
    meter = dict()
    ##If no Meter-Data available no qouta is set
    current_app.logger.debug('project_meter: response={}'.format(r.json()))
    if r.json()['entities']==[]:
        current_app.logger.debug('project_meter: Policy Engine active, no Quota set')
        meter['enabled']='false'
    else:
        meter['enabled'] = 'true'
        meter['reserved_disk'] = round(
            int(r.json()['entities'][0]['status']['resources']['reserved'].get('disk', 1))/1024/1024/1024)
        meter['utilized_disk'] = round(
            int(r.json()['entities'][0]['status']['resources']['utilized'].get('disk',0)) / 1024 / 1024 / 1024)
        current_app.logger.debug('project_meter: reserved_disk={}'.format(meter['reserved_disk']))
        if meter['reserved_disk']:
            meter['utilized_disk_percentage'] = round((meter['utilized_disk'] / meter['reserved_disk']) * 100)
        else:
            meter['utilized_disk_percentage'] = 0
        current_app.logger.debug('project_meter: utilized_disk={}'.format(meter['utilized_disk']))
        current_app.logger.debug('project_meter: utilized_disk_percentage={}'.format(meter['utilized_disk_percentage']))
        
        meter['reserved_memory'] = round(
            int(r.json()['entities'][0]['status']['resources']['reserved'].get('memory', 0))/1024/1024/1024)
        current_app.logger.debug('project_meter: reserved_memory={}'.format(meter['reserved_memory']))
        meter['utilized_memory'] = round(
            int(r.json()['entities'][0]['status']['resources']['utilized'].get('memory', 0))/1024/1024/1024)
        current_app.logger.debug('project_meter: utilized_memory={}'.format(meter['utilized_memory']))
        if meter['reserved_memory']:
            meter['utilized_memory_percentage'] = round((meter['utilized_memory']/meter['reserved_memory'])*100)
        else:
            meter['utilized_memory_percentage'] = 0
        current_app.logger.debug('project_meter: utilized_memory_percentage={}'.format(meter['utilized_memory_percentage']))
        
        meter['reserved_vcpu'] = int(r.json()['entities'][0]['status']['resources']['reserved'].get('vcpu', 0))
        current_app.logger.debug('project_meter: reserved_vcpu={}'.format(meter['reserved_vcpu']))
        meter['utilized_vcpu'] = int(r.json()['entities'][0]['status']['resources']['utilized'].get('vcpu', 0))
        current_app.logger.debug('project_meter: utilized_vcpu={}'.format(meter['utilized_vcpu']))
        if meter['reserved_vcpu']:
            meter['utilized_vcpu_percentage'] = round((meter['utilized_vcpu']/meter['reserved_vcpu'])*100)
        else:
            meter['utilized_vcpu_percentage'] = 0
        current_app.logger.debug('project_meter: utilized_vcpu_percentage={}'.format(meter['utilized_vcpu_percentage']))
    return meter
 