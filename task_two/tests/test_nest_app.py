import pytest
from flask_restful import Resource, Api, abort
from flask_sqlalchemy import SQLAlchemy
import os
from task_two.app import create_app, AllUsers, Nest
import json
from requests.auth import _basic_auth_str


@pytest.fixture
def client():

    """
    Setup of test instance
    """

    # Test db config
    basedir = os.path.abspath(os.path.dirname(__file__))
    db_path = os.path.join(basedir, 'test.db')
    db_uri = 'sqlite:///' + db_path

    # Test config
    test_config = {'TESTING': True, 'SQLALCHEMY_DATABASE_URI': db_uri, 'DEBUG': True}
    app = create_app(test_config=test_config)
    print(f"App vars: {vars(app)}")

    api = Api(app)
    db = SQLAlchemy(app)
    api.add_resource(AllUsers, '/')
    api.add_resource(Nest, '/nest/')

    with app.test_client()as client:
        yield client


def test_connect_to_app(client):

    """
    Connect to the test db
    """

    users = client.get('/')

    assert users.status_code == 200


def test_authenticated_login_fail(client):

    """
    Test authentication fail
    """

    with open('task_two/tests/t_input.json', 'r') as f:
        input = json.load(f)
    data = json.dumps({"flat": input})

    email = 'xx@xx.com'
    password = 'password'

    auth = {'Authorization': _basic_auth_str(email, password)}

    r = client.post('/nest/?order=currency&order=country&order=city&order=amount',
                    headers=auth,
                    data=data,
                    content_type='application/json')

    assert r.status_code == 401


def test_authenticated_login_success(client):

    """
    Test successful login
    """

    with open('task_two/tests/t_input.json', 'r') as f:
        input = json.load(f)

    input = json.dumps(input)
    data = json.dumps({"flat": input})

    # Test email and password
    email = 'a@admin.com'
    password = 'password'

    # Authorisation
    auth = {'Authorization': _basic_auth_str(email, password)}

    # Test post
    r = client.post('/nest/?order=currency&order=country&order=city&order=amount',
                    headers=auth,
                    data=data,
                    follow_redirects=True,
                    mimetype='application/json')
    assert r.status_code == 200