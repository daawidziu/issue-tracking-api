from itsdangerous import URLSafeTimedSerializer, BadSignature, SignatureExpired
from flask import current_app


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
