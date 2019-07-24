import pytest
import json
from unittest.mock import patch
from task_one.nest import get_nested_value, set_nested_value, create_nested_tree


def test_leaf_value_retrieval(nested_dict):

    """
    Test access of nested dict
    :param nested_dict:
    :return:
    """

    l = ['first', 'second', 'third']

    val = get_nested_value(d=nested_dict, keys=l)

    assert val == {'fourth': 'leaf', 'another': 'label'}


def test_second_level_retrieval(nested_dict):
    """
    Test access of nested dict
    :param nested_dict:
    :return:
    """

    l = ['first', 'second']

    val = get_nested_value(d=nested_dict, keys=l)

    assert val ==  {'third': {'fourth': 'leaf', 'another': 'label'} }


def test_set_nested_value(nested_dict):

    """
    Test setting the leaf value
    :param nested_dict:
    :return:
    """

    nested_dict['first']['second']['third'] = []
    l = ['first', 'second', 'third']

    leaf = {'append': 'leaf'}

    set_nested_value(d=nested_dict, keys=l, value=leaf)


    assert nested_dict == {'first': {'second': {'third': [{'append': 'leaf'}]}}}


def test_set_nested_value_with_existing_element(nested_dict):

    """
    Test setting the leaf value
    :param nested_dict:
    :return:
    """

    nested_dict['first']['second']['third'] = [{'something': 'here'}]
    l = ['first', 'second', 'third']

    leaf = {'append': 'leaf'}

    set_nested_value(d=nested_dict, keys=l, value=leaf)


    assert nested_dict == {'first': {'second': {'third': [{'something': 'here'},{'append': 'leaf'}]}}}


def test_tree_creation():

    """
    Test the creation of branches with empty list at leaf
    :return:
    """

    root = {}

    nodes = ['one', 'two', 'three']

    create_nested_tree(root=root, keys=nodes)

    assert root == {'one': {'two': {'three': []}}}


def test_leaf_insertion():

    """
    Test the creation of branches with empty list at leaf
    :return:
    """

    root = {}

    nodes = ['one', 'two', 'three']
    leaf = {'last': 'leaf'}

    create_nested_tree(root=root, keys=nodes)
    set_nested_value(d=root, keys=nodes, value=leaf )

    assert root == {'one': {'two': {'three': [leaf]}}}


def test_nested_conversion_example(json_input):

    print(f"last test: {json_input}")

    order = ['currency', 'country', 'city', 'amount']

    with open('tests/test_output.json', 'r') as f:
        output = json.load(f)

    root = {}
    for i in json_input:
        # Branch node order
        path_list = [i[o] for o in order[0:-1]]

        # The leaf value for tree
        leaf_key = order[-1]
        leaf = {leaf_key: i[leaf_key]}

        # Generate the branches
        create_nested_tree(root, path_list)

        # Populate the last element
        set_nested_value(d=root, keys=path_list, value=leaf)

    assert root == output