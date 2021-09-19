from datetime import datetime
from app.auth.models import User


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

