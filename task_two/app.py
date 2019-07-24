from flask import Flask, jsonify
from flask_restful import Resource, Api
from flask_restful.reqparse import RequestParser
import task_one.nest

import datetime

app = Flask(__name__)
api = Api(app, prefix='/api/v1')

"""
Following:
http://polyglot.ninja/rest-api-best-practices-python-flask-tutorial/
http://polyglot.ninja/securing-rest-apis-basic-http-authentication-python-flask/
"""

# Test users
users = [
    {"name": "eric", "email": "e@dev.com", "id": 0},
    {"name": "anne", "email": "a@dev.com", "id": 1}
]

# Request parsing
user_parser = RequestParser(bundle_errors=True)
user_parser.add_argument("name", type=str, required=True, help="Name has to be valid string")
user_parser.add_argument("email", type=str, required=True, help="Any email will do")
user_parser.add_argument("id", type=int, required=True, help="Please enter an integer")


class AllUsers(Resource):
    def get(self):
        payload = users
        return {"All users": payload}

    def post(self):
        args = user_parser.parse_args()
        users.append(args)
        print(f"Post method: {args}")
        return {"Created": f"{args}"}


class User(Resource):

    def get(self, id):
        rec = [user for user in users if user['id'] == id]

        if not rec:
            return {"error": "No user found"}

        return {"User details": rec[0]}

    def put(self, id):
        args = user_parser.parse_args()
        user = [user for user in users if user['id'] == id]

        print(user)

        if user:
            users.remove(user[0])
            users.append(args)

        return {"Updated": f"{args}"}

    def delete(self, id):
        user = [user for user in users if user['id'] == id]

        if user:
            users.remove(user[0])

        return {"Deleted": f"User id {id}"}


api.add_resource(AllUsers, '/')
api.add_resource(User, '/user/<int:id>')

if __name__ == '__main__':
    app.run(debug=True)