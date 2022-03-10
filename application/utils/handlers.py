from datetime import datetime, timedelta
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager, get_jwt, create_access_token, current_user, set_access_cookies

from application.models import Account


def register_handlers(app: Flask, db: SQLAlchemy, jwt: JWTManager) -> None:
    """Register application handlers"""

    @app.before_first_request
    def db_create_all():
        db.create_all()

    @app.after_request
    def refresh_expiring_jwt(response):
        try:
            exp_timestamp = get_jwt()["exp"]
            now = datetime.utcnow()
            target_timestamp = datetime.timestamp(now + timedelta(minutes=30))
            if target_timestamp > exp_timestamp:
                access_token = create_access_token(identity=current_user)
                set_access_cookies(response, access_token)
            return response
        except (RuntimeError, KeyError):
            return response

    @jwt.token_in_blocklist_loader
    def check_if_token_revoked(jwt_header, jwt_payload) -> bool:
        jti = jwt_payload['jti']
        redis = app.redis
        token = redis.get(jti)
        return token is not None

    @jwt.user_identity_loader
    def user_identity_lookup(user: Account) -> str:
        return user.public_id

    @jwt.user_lookup_loader
    def user_lookup_callback(_jwt_header, jwt_data) -> Account:
        identity = jwt_data['sub']
        return Account.get(public_id=identity)
