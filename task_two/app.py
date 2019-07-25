from flask import Flask, jsonify
from task_two.config import Config
from flask_restful import Resource, Api
from flask_restful.reqparse import RequestParser
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_httpauth import HTTPBasicAuth
from werkzeug.security import generate_password_hash, check_password_hash
import json
import sqlite3
import os
import datetime

# App, DB setup
app = Flask(__name__)
app.config.from_object(Config)
db = SQLAlchemy(app)
migrate = Migrate(app, db)
api = Api(app, prefix='/api/v1')
auth = HTTPBasicAuth()

# Import models
from task_two.models import User



# Test users
users = [
    {"name": "eric", "email": "e@dev.com", "id": 0},
    {"name": "anne", "email": "a@dev.com", "id": 1}
]

# Request parsing
user_parser = RequestParser(bundle_errors=True)
user_parser.add_argument("password", type=str, required=True, help="Name has to be valid string")
user_parser.add_argument("email", type=str, required=True, help="Any email will do")

# Flat Dict
dict_payload = RequestParser(bundle_errors=True)
dict_payload.add_argument("data", type=str, location="form", help='Send flat dict as "data: [{}, {}]"')
dict_payload.add_argument("order", action="append")

# Endpoints
class AllUsers(Resource):
    def get(self):
        payload = users
        return {"All users": payload}

    def post(self):
        args = user_parser.parse_args()
        users.append(args)
        print(f"Post method: {args}")
        return {"Created": f"{args}"}

class Nest(Resource):

    # @auth.login_required
    def post(self):

        args = dict_payload.parse_args()
        data = args.get("data")
        if data:
            data = json.loads(args["data"])



        return {"data": data,
                "order": args.get("order")}

class CreateUser(Resource):
    def post(self):
        creds = user_parser.parse_args()
        email = creds['email']
        password = creds['password']

        user = db.session.query(User).filter(User.email == email).one_or_none()

        if not user:
            hashed = generate_password_hash(password)
            u = User(email=email, password_hash=hashed)
            db.session.add(u)
            db.session.commit()

            return {"Created user": email}
        else:
            return {"User already exists"}




class AUser(Resource):

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

# Verify
@auth.verify_password
def verify(email, password):
    user = db.session.query(User).filter(User.email == email).one_or_none()
    if user:
        return  check_password_hash(user.password_hash, password)
    return False

api.add_resource(AllUsers, '/')
api.add_resource(AUser, '/user/<int:id>')
api.add_resource(Nest, '/nest')
api.add_resource(CreateUser, '/auth')


if __name__ == '__main__':
    app.run(debug=True)