from flask import Flask
from flask_login import LoginManager
from flask_restful import Api
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()
login_manager = LoginManager()

from app.resources.foo import Foo

def create_app(config_object):
    app = Flask(__name__)
    app.config.from_object(config_object)

    db.init_app(app)
    login_manager.init_app(app)

    api = Api(app)
    api.add_resource(Foo, '/')

    return app
