from flask import current_app
from uuid import uuid4

from application import db, bc
from .base import BaseModel


class Account(BaseModel):

    # Account Information
    public_id = db.Column(db.String(36), unique=True, default=lambda: str(uuid4()))
    email = db.Column(db.String(255), nullable=False, unique=True)
    password_hash = db.Column(db.String(100), nullable=False)
    verified = db.Column(db.Boolean, nullable=False, default=False)
    role = db.Column(db.String(64), nullable=False)

    @property
    def password(self):
        raise AttributeError('password: write-only field')

    @password.setter
    def password(self, password: str) -> None:
        log_rounds = current_app.config["PASSWORD_LOG_ROUNDS"]
        hash_bytes = bc.generate_password_hash(password, log_rounds)
        self.password_hash = hash_bytes.decode('utf-8')

    def validate_password(self, password: str) -> bool:
        return bc.check_password_hash(self.password_hash, password)
