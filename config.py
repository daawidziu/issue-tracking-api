from datetime import timedelta
from dotenv import load_dotenv
import os

load_dotenv()


class Config:
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    DEBUG = False
    TESTING = False
    PASSWORD_LOG_ROUNDS = os.getenv("PASSWORD_LOG_ROUNDS", 4)
    AWS_ACCESS_KEY_ID = os.getenv("AWS_ACCESS_KEY_ID")
    AWS_SECRET_ACCESS_KEY = os.getenv("AWS_SECRET_ACCESS_KEY")
    SES_REGION = os.getenv("SES_REGION")
    SES_EMAIL_SOURCE = os.getenv("SES_EMAIL_SOURCE")
    ACCESS_EXPIRES = timedelta(minutes=float(os.getenv("ACCESS_EXPIRES", 1)))
    EMAIL_MAX_AGE = int(os.getenv("EMAIL_MAX_AGE", 1))


class ProductionConfig(Config):
    SQLALCHEMY_DATABASE_URI = os.getenv("SQLALCHEMY_DATABASE_URI")
    SECRET_KEY = os.getenv("SECRET_KEY")
    SECURITY_PASSWORD_SALT = os.getenv("SECURITY_PASSWORD_SALT")
    ACCESS_EXPIRES = timedelta(minutes=float(os.getenv("ACCESS_EXPIRES", 1)))
    REDIS_URL = os.getenv("REDIS_URL", "redis://")


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
