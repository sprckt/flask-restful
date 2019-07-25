from task_one.nest import set_nested_value, create_nested_tree
import json


class Nester:

    def __init__(self, input, order):
        self.input = json.loads(input)
        self.order = order

    def nest_flat_dict(self):

        root = {}
        for i in self.input:
            # Branch node order
            path_list = [i[o] for o in self.order[0:-1]]

            # The leaf value for tree
            leaf_key = self.order[-1]
            leaf = {leaf_key: i[leaf_key]}

            # Generate the branches
            create_nested_tree(root, path_list)

            # Populate the last element
            set_nested_value(d=root, keys=path_list, value=leaf)

        root = json.dumps(root)

        return root



