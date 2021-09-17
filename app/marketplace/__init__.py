from flask import Blueprint

blueprint = Blueprint('marketplace',
                      __name__,
                      url_prefix='/marketplace')

from . import views
