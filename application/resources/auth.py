from http import HTTPStatus
from flask import request, current_app, url_for
from flask_restx import Namespace, fields, Resource, abort
from flask_jwt_extended import create_access_token, get_jwt, jwt_required

from application.models import Account
from application.utils import generate_confirmation_token, confirm_token, send_confirmation, \
    check_if_token_revoked, user_lookup_callback, user_identity_lookup

auth_ns = Namespace('auth', description='Authentication related operations.')

email_pattern = r'[^@]+@[^@]+\.[^@]+'
password_pattern = r'^(?=.*[0-9])(?=.*[a-zA-Z]).{8,}$'

user_auth = auth_ns.model('UserAuth', {
    'email': fields.String('User email', pattern=email_pattern, required=True),
    'password': fields.String('User password', pattern=password_pattern, required=True),
}, strict=True)


@auth_ns.route('/register')
class Register(Resource):

    @auth_ns.expect(user_auth, validate=True)
    @auth_ns.response(int(HTTPStatus.CREATED), 'New user successfully registered')
    @auth_ns.response(int(HTTPStatus.CONFLICT), 'Email address is already registered')
    @auth_ns.response(int(HTTPStatus.BAD_REQUEST), 'Validation Error')
    @auth_ns.response(int(HTTPStatus.INTERNAL_SERVER_ERROR), 'Internal server error')
    def post(self):
        """Registers a new user and return access token"""
        data = request.get_json()

        if Account.get(email=data['email']):
            abort(HTTPStatus.CONFLICT, '{} is already registered'.format(data['email']))

        account = Account(email=data['email'], password=data['password'], role="User")
        account.save()

        access_token = create_access_token(identity=account)
        confirmation_token = generate_confirmation_token(account.email)

        confirmation_url = url_for("api.auth_confirm", token=confirmation_token, _external=True)
        current_app.q.enqueue(send_confirmation, account.email, confirmation_url)

        return {'access_token': access_token}, 201


@auth_ns.route('/login')
class Login(Resource):

    @auth_ns.expect(user_auth)
    @auth_ns.response(int(HTTPStatus.OK), 'Login succeeded')
    @auth_ns.response(int(HTTPStatus.UNAUTHORIZED), 'Wrong username or password')
    @auth_ns.response(int(HTTPStatus.BAD_REQUEST), 'Validation Error')
    @auth_ns.response(int(HTTPStatus.INTERNAL_SERVER_ERROR), 'Internal server error')
    def post(self):
        """Login user and return access token"""
        data = request.get_json()

        account = Account.get(email=data['email'])
        if not account or not account.validate_password(data['password']):
            abort(HTTPStatus.UNAUTHORIZED, 'Wrong username or password')

        access_token = create_access_token(identity=account)

        return {'access_token': access_token}, 200


@auth_ns.route('/logout')
class Logout(Resource):

    @jwt_required()
    @auth_ns.response(int(HTTPStatus.OK), 'Logout succeeded, token is no longer valid')
    @auth_ns.response(int(HTTPStatus.UNAUTHORIZED), 'Token is invalid or expired')
    @auth_ns.response(int(HTTPStatus.UNPROCESSABLE_ENTITY), 'Bad Authentication Token')
    @auth_ns.response(int(HTTPStatus.BAD_REQUEST), 'Validation Error')
    @auth_ns.response(int(HTTPStatus.INTERNAL_SERVER_ERROR), 'Internal server error')
    def post(self):
        """Logout user and block token"""
        jti = get_jwt()['jti']
        current_app.redis.set(jti, "", ex=current_app.config['ACCESS_EXPIRES'])
        return '', 200


@auth_ns.route('/confirm/<token>')
class Confirm(Resource):

    @auth_ns.response(int(HTTPStatus.OK), 'Successfully confirmed user')
    @auth_ns.response(int(HTTPStatus.UNAUTHORIZED), 'Wrong confirmation url')
    @auth_ns.response(int(HTTPStatus.UNPROCESSABLE_ENTITY), 'Bad Authentication Token')
    @auth_ns.response(int(HTTPStatus.BAD_REQUEST), 'Validation Error')
    @auth_ns.response(int(HTTPStatus.INTERNAL_SERVER_ERROR), 'Internal server error')
    def get(self, token):
        """Confirm user registration"""

        email = confirm_token(token)

        if not email:
            return int(HTTPStatus.UNAUTHORIZED)

        account = Account.get(email=email)
        account.update({'verified': True})

        return '', 200
