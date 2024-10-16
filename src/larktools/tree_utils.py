from lark import Tree
from lark import Token


def is_rule(node):
    """Determine whether a rule node."""
    return isinstance(node, Tree)


def is_terminal(node):
    """Determine whether terminal node."""
    return isinstance(node, Token)


def get_name(node):
    """ Get the name of the node."""
    if is_rule(node):
        return node.data
    elif is_terminal(node):
        return node.type
    else:
        raise TypeError(
            "Node must be an instance of lark.Tree or lark.Token"
        )


def get_children(node):
    """Get a list of children from a rule node."""
    return node.children

def get_first_child(node):
    """Get the first child from a rule node."""
    children = get_children(node)
    assert len(children) > 0
    return children[0]

def get_value(node):
    """Get the value associated with a terminal node."""
    return node.value
