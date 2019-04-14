from datetime import datetime

from bs4 import BeautifulSoup
from flask import abort, request
from flask.json import jsonify
from flask_httpauth import HTTPBasicAuth, HTTPTokenAuth
from flask_restful import Resource, reqparse
import requests

from app import db
from app.resources.users import User

httpauth = HTTPBasicAuth()
tokenauth = HTTPTokenAuth()

@httpauth.verify_password
def verify_pw(username, password):
    user = User.query.filter(User.username == username).first()
    return user is not None and user.check_password(password)


@tokenauth.verify_token
def verify_token(token):
    user = User.query.filter_by(token=token).first()
    if user is None or user.token_expiry < datetime.utcnow():
        return False
    return True


class Register(Resource):
    def post(self):
        data = request.json
        if 'username' not in data or 'password' not in data:
            abort(404)  # username and/or password not provided
        username, password = data['username'], data['password']
        if User.query.filter(User.username == username).first() is not None:
            abort(404)  # non-unique username
        user = User(username=username)
        user.set_password(password)
        db.session.add(user)
        db.session.commit()
        return jsonify("User successfully added")


class GetToken(Resource):
    @httpauth.login_required
    def get(self):
        user = User.query.filter(User.username == request.authorization.username).first()
        if user is None:
            abort(404)
        user.set_token()
        db.session.commit()
        return jsonify(token=user.token)


class GetNews(Resource):
    @tokenauth.login_required
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('source', choices=['bbc', 'guardian'])
        args = parser.parse_args()
        print(args)
        if args['source'] == 'bbc':
            response = requests.get('https://www.bbc.co.uk/news')
            if response.status_code == 200:
                soup = BeautifulSoup(response.content, 'html.parser')
                items = soup.find('div', class_="nw-c-most-read__items gel-layout gel-layout--no-flex").find('ol').contents
                return {'articles:': [article.text for article in items]}, 201
            else:
                return {"message": "could not parse page"}, 500
        if args['source'] == 'guardian':
            response = requests.get('https://www.theguardian.com/uk')
            if response.status_code == 200:
                soup = BeautifulSoup(response.content, 'html.parser')
                items = soup.find_all('span', class_="js-headline-text")[:10]
                return {'articles:': [article.text for article in items]}, 201
            else:
                return {"message": "could not parse page"}, 500
