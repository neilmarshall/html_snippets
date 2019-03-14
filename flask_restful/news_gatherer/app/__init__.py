from flask import Flask
from flask_restful import Api
from app.resources.news import GetNews

def create_app():
    app = Flask(__name__)
    api = Api(app)
    api.add_resource(GetNews, '/get_news')
    return app
