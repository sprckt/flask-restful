import pytest
import json

@pytest.fixture(scope='function')
def json_input():
    with open('input.json', 'r') as f:
        input = json.load(f)

    print(f"Input: {input}")

    return input


@pytest.fixture(scope='function')
def nested_dict():
    return {'first': {'second': {'third': {'fourth': 'leaf', 'another': 'label'}}}}

