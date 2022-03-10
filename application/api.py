from flask import Blueprint
from flask_restx import Api

from application.resources import auth_ns, projects_ns, issues_ns

api_bp = Blueprint('api', __name__, url_prefix='')
authorizations = {
    'apiKey': {
        'type': 'apiKey',
        'in': 'header',
        'name': 'X-CSRF-Token'
    }
}

api = Api(
    app=api_bp,
    title='Issue Tracker',
    version='1.0',
    description='REST Api for issues tracking',
    security='apiKey',
    authorizations=authorizations
)

api.add_namespace(auth_ns)
api.add_namespace(projects_ns)
api.add_namespace(issues_ns)
