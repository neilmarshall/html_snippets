from flask import Flask
from config import Config
from app.models import db
from app.routes import homepage


def create_app(config_object=Config):

    app = Flask(__name__)
    app.config.from_object(config_object)

    app.register_blueprint(homepage)

    db.init_app(app)

    return app
