from itsdangerous import URLSafeTimedSerializer, BadSignature, SignatureExpired
from flask import Flask, current_app

from application import jwt
from application.models import Account


@jwt.token_in_blocklist_loader
def check_if_token_revoked(jwt_header, jwt_payload) -> bool:
    jti = jwt_payload['jti']
    redis = current_app.redis
    token = redis.get(jti)
    return token is not None


@jwt.user_identity_loader
def user_identity_lookup(user: Account) -> str:
    return user.public_id


@jwt.user_lookup_loader
def user_lookup_callback(_jwt_header, jwt_data) -> Account:
    identity = jwt_data['sub']
    return Account.get(public_id=identity)


def generate_confirmation_token(email: str) -> str | bytes:
    """Generate email account confirmation token"""
    serializer = URLSafeTimedSerializer(current_app.config["SECRET_KEY"])
    return serializer.dumps(email, salt=current_app.config["SECURITY_PASSWORD_SALT"])


def confirm_token(token: str) -> str | bool:
    """Validate confirmation token"""
    serializer = URLSafeTimedSerializer(current_app.config["SECRET_KEY"])
    try:
        email = serializer.loads(token, salt=current_app.config["SECURITY_PASSWORD_SALT"],
                                 max_age=current_app.config["EMAIL_MAX_AGE"])
    except BadSignature:
        return False
    except SignatureExpired:
        return False
    return email
