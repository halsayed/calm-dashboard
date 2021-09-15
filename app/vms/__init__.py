from flask import Blueprint

blueprint = Blueprint('vms',
                      __name__,
                      url_prefix='/vms')

from . import views
