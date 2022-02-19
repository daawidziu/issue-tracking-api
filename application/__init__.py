from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from flask_jwt_extended import JWTManager
from flask_bcrypt import Bcrypt

import config

db = SQLAlchemy()
ma = Marshmallow()
jwt = JWTManager()
bc = Bcrypt()


def init_app(config_file: object | str = config.DevelopmentConfig) -> Flask:
    app = Flask(__name__)
    app.config.from_object(config_file)

    db.init_app(app)
    ma.init_app(app)
    jwt.init_app(app)
    bc.init_app(app)

    return app
