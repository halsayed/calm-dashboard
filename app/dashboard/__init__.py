from flask import Blueprint

blueprint = Blueprint('dashboard',
                      __name__,
                      url_prefix='')

from . import views
