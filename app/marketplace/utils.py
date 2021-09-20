from app.auth.models import User
import uuid
import re
from flask import current_app

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

def get_runtime_editables(mpi_uuid, user: User):
    r = user.api_get('calm_marketplace_items/{}'.format(mpi_uuid))
    data = r.json()['spec']['resources']['app_blueprint_template']['status']['resources']['app_profile_list'][0]['variable_list']
    current_app.logger.debug('get runtime editables (AA): {}'.format(data))
    runtime_editables =[]
    for variable in data:
        runtime_editables.append({
            'name': variable['name'],
            'uuid': variable['uuid'],
            'value': variable['value']
        })
    return runtime_editables

def launch_mpi(mpi_uuid, app_name, runtime_editables,  user: User):
    bp_spec = {}
    current_app.logger.debug('launch_mpi:mpi_uuid={}'.format(mpi_uuid))
    ## ToDo: Actual Deployment will always be in first assigned Project (if multiple)
    payload = {
        'kind': 'project'
    }
    r = user.api_post('projects/list', payload)
    project_uuid = r.json()['entities'][0]['metadata']['uuid']
    r = user.api_get('projects/{}'.format(project_uuid))
    env_uuid = r.json()['status']['resources']['environment_reference_list'][0]['uuid']
    r = user.api_get('calm_marketplace_items/{}'.format(mpi_uuid))
    data = r.json()
    mpi_name = data['status']['name']
    NAME_RE = re.compile("[.|\s]+")
    bp_spec['spec'] = data['spec']['resources']['app_blueprint_template']['spec']
    del bp_spec['spec']['name']
    bp_spec['spec']['environment_uuid'] = env_uuid
    #Generate bp name as per user logic
    bp_name = "mpi_%s_%s" % (mpi_name.replace(".|\s", "_"), str(uuid.uuid4())[-7:])
    bp_spec['spec']['app_blueprint_name'] = "mpi_%s_%s" % (re.sub(NAME_RE,"_",mpi_name), str(uuid.uuid4())[-7:])
    bp_spec['metadata'] = {
        "kind": "blueprint",
        "project_reference": {
            "kind": "project",
            "uuid": project_uuid
        },
        "categories": data["metadata"]["categories"]
    }
    bp_spec['api_version'] = "3.0"

    r = user.api_post('blueprints/marketplace_launch',bp_spec)
    response = r.json()
    del response["spec"]["environment_uuid"]
    bp_uuid = response['metadata']['uuid']
    
    ##deploy app
    payload = response
    del payload['spec']['name']
    del payload['status']
    payload['spec']['application_name'] = app_name
    payload['spec']['app_profile_reference'] = {'kind': 'app_profile', 'uuid':payload['spec']['resources']['app_profile_list'][0]['uuid']}
    ##edit Variables if needed
    editables = payload['spec']['resources']['app_profile_list'][0]['variable_list']
    current_app.logger.debug('runtime_editables from View (AA): {}'.format(runtime_editables))
    current_app.logger.debug('launch mpi editables (AA): {}'.format(editables))
    

    new_editables = []
    for var1 in editables:
        for var2 in runtime_editables:
            if var1['name'] in var2:
                var1['value']=var2[var1['name']]
            new_editables.append(var1)
            
    current_app.logger.debug('finished editables={}'.format(new_editables))
    payload['spec']['resources']['app_profile_list'][0]['variable_list'] = new_editables

    r = user.api_post('blueprints/{}/launch'.format(bp_uuid),payload)
    response = r.json()
    return response


    
