from flask import Flask
from flask_restful import Api
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

from app.resources.news import GetNews, GetToken, Register

def create_app(config_object):
    app = Flask(__name__)
    app.config.from_object(config_object)

    db.init_app(app)

    api = Api(app)
    api.add_resource(GetNews, '/get_news')
    api.add_resource(GetToken, '/token')
    api.add_resource(Register, '/register')

    return app
