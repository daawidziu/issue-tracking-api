from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow

import config

db = SQLAlchemy()
ma = Marshmallow()


def init_app(config_file: object | str = config.DevelopmentConfig) -> Flask:
    app = Flask(__name__)
    app.config.from_object(config_file)

    db.init_app(app)
    ma.init_app(app)

    return app
