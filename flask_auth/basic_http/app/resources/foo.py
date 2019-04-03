from flask_login import login_required
from flask_restful import Resource

class Foo(Resource):
    @login_required
    def get(self):
        return {"content": "top secret information"}, 200
