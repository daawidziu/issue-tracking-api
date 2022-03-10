import rq
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from flask_jwt_extended import JWTManager
from flask_bcrypt import Bcrypt
from flask_migrate import Migrate
from flask_mail import Mail
from redis import Redis


db = SQLAlchemy()
ma = Marshmallow()
jwt = JWTManager()
bc = Bcrypt()
migrate = Migrate()
mail = Mail()


def init_app(config_file: object | str = 'config.ProductionConfig') -> Flask:
    app = Flask(__name__)
    app.config.from_object(config_file)

    app.redis = Redis.from_url(app.config["REDIS_URL"])
    app.q = rq.Queue("task-queue", connection=app.redis)

    db.init_app(app)
    ma.init_app(app)
    jwt.init_app(app)
    bc.init_app(app)
    migrate.init_app(app, db)
    mail.init_app(app)

    with app.app_context():
        from application.utils import register_handlers
        from application.api import api_bp

        register_handlers(app, db, jwt)
        app.register_blueprint(api_bp)

    return app
