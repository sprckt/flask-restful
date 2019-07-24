#!/usr/bin/env python3

import json
import os
import argparse
import logging
import sys
from collections import defaultdict
from functools import reduce
from pprint import pprint
import json

logging.basicConfig(
        level=logging.DEBUG,
        format='%(asctime)s:%(levelname)s:%(filename)s:%(lineno)d:%(message)s'
        )

print(f'Source dir: {os.getcwd()}')

def parse_args():

    """
    Command line args
    :return: Args
    """

    parser = argparse.ArgumentParser()

    parser.add_argument('order',
                        nargs='*',
                        help='List out the nested keys in the order that they should be nested')

    return parser.parse_args()


def read_from_stdin():

    """
    Get JSON array from stdin
    :return:
    """
    file = sys.stdin

    j_file = json.load(file)

    return j_file


def get_nested_value(d, keys):

    """
    Dynamically retrieve the inner-most value of a nested dict
    :param d: The dictionary
    :param keys: List of nested keys
    :return:
    """

    for key in keys:
        d = d[key]

    return d


def set_nested_value(d, keys, value):

    """
    Dynamically append the leaf value
    :param d: Source dictionary
    :param keys: List of nested keys
    :param value: The leaf value to append to inner most level
    :return:
    """

    print(keys)
    d = get_nested_value(d, keys[:-1])
    d[keys[-1]].append(value)

    return

def create_nested_tree(root, keys):


    num_keys = len(keys)
    for ix, key in enumerate(keys, 1):

        # Nested dicts all the way down except for....
        if ix < num_keys:
            root = root.setdefault(key, {})
        # The innermost level, which will be a list - leaf values should append to this list
        else:
            root = root.setdefault(key, [])

    return 

def main():

    args = parse_args()
    order = args.order

    logging.debug(f"Args: {vars(args)}")

    input = read_from_stdin()
    print(f"Input: \n{input}")

    root = {}
    for i in input:
        # Branch node order 
        path_list = [i[o] for o in order[0:-1]]

        # The leaf value for tree
        leaf_key = order[-1]
        leaf = {leaf_key: i[leaf_key]}

        # Generate the branches
        create_nested_tree(root, path_list)

        # Populate the last element
        set_nested_value(d=root, keys=path_list, value=leaf)


    json_fmt = json.dumps(root)

    with open('output.json', 'w+') as f:
        json.dump(root, f)

    print(f"Path list: {path_list}")
    print(f"Nested dict from function:")
    pprint(json_fmt)


if __name__ == '__main__':
    main()
