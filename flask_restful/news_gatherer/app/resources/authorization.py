from datetime import datetime

from flask import abort, g, request
from flask.json import jsonify
from flask_httpauth import HTTPBasicAuth, HTTPTokenAuth
from flask_restful import Resource

from app import db
from app.resources.models import User

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
    g.current_user = user  # set current user on global object
    return True


class Register(Resource):
    def post(self):
        data = request.json
        if 'username' not in data or 'password' not in data:
            abort(404)  # username and/or password not provided
        username, password = data['username'], data['password']
        if not username or not password:
            abort(404)  # blank username and/or password
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
