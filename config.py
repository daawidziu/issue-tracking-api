from datetime import timedelta
from dotenv import load_dotenv
import os

load_dotenv()


class Config:
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    DEBUG = False
    TESTING = False
    PASSWORD_LOG_ROUNDS = os.getenv("PASSWORD_LOG_ROUNDS", 4)
    JWT_ACCESS_TOKEN_EXPIRES = int(os.getenv("JWT_ACCESS_TOKEN_EXPIRES", 15))
    EMAIL_MAX_AGE = int(os.getenv("EMAIL_MAX_AGE", 1))
    REDIS_URL = os.getenv("REDIS_URL", "redis://")
    JWT_TOKEN_LOCATION = ['cookies']
    JWT_COOKIE_SECURE = True
    MAIL_SERVER = 'smtp.gmail.com'
    MAIL_PORT = 465
    MAIL_USERNAME = os.getenv('MAIL_USERNAME')
    MAIL_PASSWORD = os.getenv('MAIL_PASSWORD')
    JWT_COOKIE_DOMAIN = os.getenv('JWT_COOKIE_DOMAIN', None)
    MAIL_USE_TLS = False
    MAIL_USE_SSL = True


class ProductionConfig(Config):
    SQLALCHEMY_DATABASE_URI = os.getenv("SQLALCHEMY_DATABASE_URI")
    SECRET_KEY = os.getenv("SECRET_KEY")
    SECURITY_PASSWORD_SALT = os.getenv("SECURITY_PASSWORD_SALT")


class DevelopmentConfig(Config):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = os.getenv("SQLALCHEMY_DATABASE_URI", "sqlite:///dev.db")
    SECRET_KEY = os.getenv("SECRET_KEY", "NotReallyASecret")
    SECURITY_PASSWORD_SALT = os.getenv("SECURITY_PASSWORD_SALT", "AgainNotReallyASecret")


class TestingConfig(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = os.getenv("SQLALCHEMY_DATABASE_URI", "sqlite:///test.db")
    SECRET_KEY = os.getenv("SECRET_KEY", "NotReallyASecret")
    SECURITY_PASSWORD_SALT = os.getenv("SECURITY_PASSWORD_SALT", "AgainNotReallyASecret")
