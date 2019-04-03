from flask import Flask
from flask_restful import Api

from app.resources.foo import Foo

def create_app(config_object):
    app = Flask(__name__)
    app.config.from_object(config_object)

    api = Api(app)
    api.add_resource(Foo, '/')

    return app
