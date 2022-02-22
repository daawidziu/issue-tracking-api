from flask import Blueprint
from flask_restx import Api

from application.resources import auth_ns

api_bp = Blueprint('api', __name__, url_prefix='/issue-tracker')
authorizations = {
    'Bearer Auth': {
        'type': 'apiKey',
        'in': 'header',
        'name': 'Authorization'
    }
}

api = Api(
    app=api_bp,
    title='Issue Tracker',
    version='0.1',
    description='TODO',
    security='Bearer Auth',
    authorizations=authorizations
)

api.add_namespace(auth_ns)
