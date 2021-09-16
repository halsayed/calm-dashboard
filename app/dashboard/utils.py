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

def list_marketplace_items(user: User) -> list:
    """
    Returns a list of available Marketplace Items
    :param user:
    :return:
    """
    payload = {
        'filter_criteria': 'marketplace_item_type_list==APP;(app_state==PUBLISHED)',
        'entity_type': 'marketplace_item',
        'group_member_attributes': [{'attribute': 'name'}]
    }
    r = user.api_post('groups', payload)
    published_list = []
    for entity_item in r.json()['group_results'][0]['entity_results']:
        blueprint_name = ''
        # check for name field
        for field in entity_item['data']:
            if field.get('name', None) == 'name':
                blueprint_name = field['values'][0]['values'][0]

        # check if the blueprint name is in the prefix list
        #if blueprint_name[0] == '_':
        #    blueprint_prefix = blueprint_name[1:blueprint_name.find('_', 1)]
        #if blueprint_prefix in prefix_list:
        published_list.append({ 'uuid': entity_item['entity_id'],
                                'name': blueprint_name,
                                'display_name': blueprint_name[blueprint_name.find('_', 1)+1:]
                                })

    return published_list 
