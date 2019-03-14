#! venv/bin/python3.7

from bs4 import BeautifulSoup
import requests

from flask import Flask, request
from flask_restful import Api, Resource, inputs, reqparse

app = Flask(__name__)
api = Api(app)

class HelloWorld(Resource):
    def get(self):
        return {'hello': 'world'}

    def post(self):
        return {'You posted: ': request.form['data']}, 201


class Multiply(Resource):
    def get(self, a, b):
        return {'response': a * b}


class DateParser(Resource):
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('date', type=inputs.date)
        args = parser.parse_args()
        date = args['date']
        return {'date:': str(date)}


api.add_resource(HelloWorld, '/')
api.add_resource(Multiply, '/multiply/<int:a>/<int:b>')
api.add_resource(DateParser, '/date')

if __name__ == '__main__':
    app.run(debug=True)
