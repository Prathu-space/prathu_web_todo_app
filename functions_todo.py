import json
import os
def get_todos(filepath="Todo.txt"):
    """ Read a text file and return the list of
    to-do items.
    """
    if not os.path.exists(filepath) or os.stat(filepath).st_size == 0:
        return []
    with open(filepath, 'r') as file_local:
        return json.load(file_local)


def write_todos(todos_arg, filepath="Todo.txt"):
    """ Write the to-do items list in the text file."""
    with open(filepath, 'w') as file:
        json.dump(todos_arg, file)


if __name__ == "__main__":
    print("Hello from functions!")
    print(get_todos())