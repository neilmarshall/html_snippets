import hashlib

from flask import jsonify
from flask_httpauth import HTTPBasicAuth, HTTPTokenAuth
from flask_restful import Resource

httpauth = HTTPBasicAuth()
tokenauth = HTTPTokenAuth()

users = {'test_user': 'd74ff0ee8da3b9806b18c877dbf29bbde50b5bd8e4dad7a3a725000feb82e8f1'}  # sha256 encoding of 'pass'
tokens = {'5e884898da28047151d0e56f8dc6292773603d0d6aabbdd62a11ef721d1542d8'}  # sha256 encoding of 'password'

@httpauth.verify_password
def verify_pw(username, password):
    if username in users:  # in reality we would check the username and password hash versus what's stored in a database
        hashed_password = hashlib.sha256(bytes(password, 'utf-8')).hexdigest()
        return users.get(username) == hashed_password
    return None


@tokenauth.verify_token
def verify_token(token):
    return token in tokens  # in reality we would check the token against a database, including checking the token has not expired


class Foo(Resource):
    @tokenauth.login_required
    def get(self):
        return {"content": "top secret information -- protected by token"}, 200


class Token(Resource):
    @httpauth.login_required
    def get(self):
        return {"token": list(tokens)[0]}, 200
