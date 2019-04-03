from flask_restful import Resource

class Foo(Resource):
    def get(self):
        return {"content": "top secret information"}, 200
