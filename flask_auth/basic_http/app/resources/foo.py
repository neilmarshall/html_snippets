import hashlib

from flask_httpauth import HTTPBasicAuth
from flask_restful import Resource

auth = HTTPBasicAuth()

users = {'test_user': 'd74ff0ee8da3b9806b18c877dbf29bbde50b5bd8e4dad7a3a725000feb82e8f1'}  # sha256 encoding of 'pass'

@auth.verify_password
def verify_pw(username, password):
    if username in users:
        hashed_password = hashlib.sha256(bytes(password, 'utf-8')).hexdigest()
        return users.get(username) == hashed_password
    return None


class Foo(Resource):
    @auth.login_required
    def get(self):
        return {"content": "top secret information"}, 200
