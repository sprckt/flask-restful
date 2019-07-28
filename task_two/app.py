from flask import Flask
from task_two.config import Config
from flask_restful import Resource, Api, abort
from flask_restful.reqparse import RequestParser
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_httpauth import HTTPBasicAuth
from werkzeug.security import generate_password_hash, check_password_hash
import json
import os
from task_two.processor import Nester

# App, DB setup
def create_app(test_config=None):
    app = Flask(__name__)
    app.config.from_object(Config)


    if test_config is None:
        # load the instance config, if it exists, when not testing
        app.config.from_pyfile('config.py', silent=True)
    else:
        # load the test config if passed in
        app.config.from_mapping(test_config)

    # ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass


    return app

# Instantiate service
app = create_app()
db = SQLAlchemy(app)
api = Api(app)
auth = HTTPBasicAuth()

# Import models
from task_two.models import User


# Request parsing
user_parser = RequestParser(bundle_errors=True)
user_parser.add_argument("password", type=str, required=True, help="Name has to be valid string")
user_parser.add_argument("email", type=str, required=True, help="Any email will do")

# Flat Dict
dict_payload = RequestParser(bundle_errors=True)
dict_payload.add_argument("flat", location=["form", "json", "files"], help='Send flat dict as "data: [{}, {}]"')
dict_payload.add_argument("order", action="append")

# Endpoints
class AllUsers(Resource):
    def get(self):
        users = db.session.query(User).all()
        users = [u.email for u in users]
        print(users)
        return {"All users": users}


class Nest(Resource):

    @auth.login_required
    def post(self):

        args = dict_payload.parse_args()
        data = args.get("flat")

        key_order = args.get("order")
        if data:
            data = json.loads(args["flat"])
            print(f"Data for app: {data}")
        else:
            abort(400, message='No data provided')

        nested = Nester(input=data, order=key_order)

        try:
            nested = nested.nest_flat_dict()
        except KeyError:
            abort(422, messsage="Key in ordered list not found in flat dict")

        return {"data": data,
                "order": key_order,
                "nested_dict": nested}

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

# Verify
@auth.verify_password
def verify(email, password):
    user = db.session.query(User).filter(User.email == email).one_or_none()
    if user:
        return  check_password_hash(user.password_hash, password)
    return False

api.add_resource(AllUsers, '/')
api.add_resource(Nest, '/nest')
api.add_resource(CreateUser, '/auth')


if __name__ == '__main__':
    app.run(debug=True)
    print('Running MAIN')