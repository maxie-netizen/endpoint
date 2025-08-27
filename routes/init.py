from flask import Blueprint

main = Blueprint('main', __name__)
auth = Blueprint('auth', __name__)
api = Blueprint('api', __name__)
dashboard = Blueprint('dashboard', __name__)

from . import main_routes, auth_routes, api_routes, dashboard_routes
