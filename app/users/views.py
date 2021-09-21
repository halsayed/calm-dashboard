from flask import render_template, current_app, abort
from flask_login import login_required, current_user

from .utils import get_project_user_groups
from . import blueprint


@blueprint.route('/')
@login_required
def index():
    # if user is not an admin raise an error
    if not current_user.is_admin:
        abort(403)

    groups = get_project_user_groups(current_user)
    return render_template('users/index.html', segment=['users'], groups=groups)
