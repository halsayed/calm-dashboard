from requests.cookies import RequestsCookieJar
from datetime import datetime

from constants import NTNX_COOKIE, UNDEFINED_PROJECT_CODE


def extract_cookie_details(cookies: RequestsCookieJar) -> (str, datetime):
    """
    Extract Nutanix prism cookie (value and expiry)
    :param cookies:
    :return:
    """
    value = None
    expires = None
    for cookie in cookies:
        if cookie.name == NTNX_COOKIE:
            value = cookie.value
            expires = datetime.fromtimestamp(cookie.expires)

    return value, expires


def expand_project_name(project_name: str) -> (str, str):
    """
    Extract project name and short code from Calm project name
    e.g: Calm project name: ABC_Project X -> will return
            project_code: ABC
            project_name: Project X
    :param project_name:
    :return:
    """
    i = project_name.find('_')
    if i > 0:
        code = project_name[:i].upper()
        name = project_name[i+1:]
    else:
        code = UNDEFINED_PROJECT_CODE
        name = project_name

    return code, name

