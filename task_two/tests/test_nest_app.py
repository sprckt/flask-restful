import pytest
from flask_restful import Resource, Api, abort
from flask_sqlalchemy import SQLAlchemy
from task_two.app import create_app, AllUsers, Nest
import os
from task_two.app import create_app, AllUsers, Nest
from task_two.models import User, db as models_db
import json
from requests.auth import _basic_auth_str


@pytest.fixture
def client():

    basedir = os.path.abspath(os.path.dirname(__file__))
    db_path = os.path.join(basedir, 'test.db')
    db_uri = 'sqlite:///' + db_path

    print(f"DB Path: {db_path}")

    test_config = {'TESTING': True, 'SQLALCHEMY_DATABASE_URI': db_uri, 'DEBUG': True}
    app = create_app(test_config=test_config)
    print(f"App vars: {vars(app)}")

    api = Api(app)
    db = SQLAlchemy(app)
    api.add_resource(AllUsers, '/')
    api.add_resource(Nest, '/nest')


    with app.test_client()as client:
        users = db.session.query(User).all()
        print(f"From db: {users} | {vars(db)}")
        yield client


def test_connect_to_db(client):

    """Connect to the test db"""

    users = client.get('/')
    print(f"Users: {users.status_code} {users.json}")

    assert users.status_code == 200


def test_authenticated_login_fail(client):

    """Test authentication fail"""

    with open('task_two/tests/t_input.json', 'r') as f:
        input = json.load(f)
    data = json.dumps({"flat": input})

    email = 'xx@xx.com'
    password = 'password'

    auth = {'Authorization': _basic_auth_str(email, password)}

    print(f"Auth: {auth}")

    r = client.post('/nest?order=currency&order=country&order=city&order=amount',
                    headers=auth,
                    data=data,
                    content_type='application/json')

    assert r.status_code == 401


def test_authenticated_login_success(client):

    with open('task_two/tests/t_input.json', 'r') as f:
        input = json.load(f)
    data = json.dumps({"flat": input})

    email = 'a@admin.com'
    password = 'password'

    auth = {'Authorization': _basic_auth_str(email, password)}

    print(f"Auth: {auth}")

    r = client.post('/nest?order=currency&order=country&order=city&order=amount',
                    headers=auth,
                    json=data)
    print(vars(r))
    assert r.status_code == 200