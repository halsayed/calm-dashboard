from flask import current_app
from app.auth.models import User


def get_project_user_groups(user: User) -> dict:
    """
    Get the user groups assigned to this project

    :param user:
    :return:
    """
    r = user.api_get(f'projects/{user.project_uuid}')
    current_app.logger.debug(f'Project GET API status code {r.status_code}')
    current_app.logger.debug(f'API call result: {r.content}')
    user_groups = {}

    if r.status_code == 200:
        for group in r.json()['status']['resources']['external_user_group_reference_list']:
            user_groups[group['uuid']] = {'name': group['name']}

    # Get Prism role for each group
    for group_uuid in user_groups:
        r = user.api_get(f'user_groups/{group_uuid}')
        if r.status_code == 200:
            acp = r.json()['status']['resources']['access_control_policy_reference_list']
            if len(acp):
                user_groups[group_uuid]['apc_uuid'] = acp[0]['uuid']

    return user_groups
