from flask_httpauth import HTTPBasicAuth
from flask_restful import Resource

auth = HTTPBasicAuth()

users = {'test_user': 'pass'}

@auth.get_password
def get_pw(username):
    if username in users:
        return users.get(username)
    return None


class Foo(Resource):
    @auth.login_required
    def get(self):
        return {"content": "top secret information"}, 200
