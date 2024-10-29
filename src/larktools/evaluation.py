from typing import Callable

from functools import reduce
from lark import Lark, Token

from .ebnf_grammar import grammar
from .tree_utils import (
    is_rule,
    is_terminal,
    get_name,
    get_children,
    get_first_child,
    get_value,
)


def instantiate_eval_tree(lark_node):
    node_name = get_name(lark_node)
    # tunnel thorugh dummy nodes, e.g. sum, product
    while node_name not in INV_NODE_MAP:
        if isinstance(lark_node, Token):
            raise AttributeError(
                f"`{lark_node.type}` is a terminal node"
                "and doesn't have a node class associated with it."
            )
        if len(lark_node.children) != 1:
            raise IndexError(
                "Nodes without associated node class "
                "must have exactly one child. However, "
                f"the node `{get_name(lark_node)}` has "
                f"{len(lark_node.children)} children."
            )
        lark_node = lark_node.children[0]
        node_name = get_name(lark_node)

    return INV_NODE_MAP[node_name](lark_node)


class RootNode:
    def __init__(self, lark_node):
        self._children = [
            instantiate_eval_tree(n) for n in lark_node.children
        ]

    def __call__(self, env):
        results = [n(env) for n in self._children]
        return results[-1]


class AssignNode:
    def __init__(self, lark_node):
        self._varname = get_value(lark_node.children[0])
        self._expr = instantiate_eval_tree(lark_node.children[1])

    def __call__(self, env):
        env[self._varname] = self._expr(env)


class VariableNode:
    def __init__(self, lark_node):
        self._varname = get_value(lark_node.children[0])
        self._index_nodes = [
            instantiate_eval_tree(n) for n in lark_node.children[1:]
        ]

    def __call__(self, env):
        index_values = [n(env) for n in self._index_nodes]
        return reduce(
            lambda lst, idx: lst[idx], index_values, env[self._varname]
        )


class NumberNode:
    def __init__(self, lark_node):
        node_name = get_name(lark_node)
        self._value = {
            "SIGNED_FLOAT": float, "INT": int, "INDEX": int,
        }[node_name](get_value(lark_node))

    def __call__(self, env):
        return self._value


class MappedOperatorNode:
    def __init__(self, lark_node, op_map):
        node_name = get_name(lark_node)
        self._children = [
            instantiate_eval_tree(n) for n in lark_node.children
        ]
        self._func = op_map[node_name]

    def __call__(self, env):
        results = [n(env) for n in self._children]
        return self._func(results)


class UnaryOperatorNode(MappedOperatorNode):
    def __init__(self, lark_node):
        super().__init__(
            lark_node,
            op_map={"neg_atom": lambda x: -x[0]}
        )


class BinaryOperatorNode(MappedOperatorNode):
    def __init__(self, lark_node):
        super().__init__(
            lark_node,
            op_map = {
                "addition": lambda x: sum(x),
                "subtraction": lambda x: x[0] - x[1],
                "multiplication": lambda x: x[0] * x[1],
                "division": lambda x: x[0] / x[1],
            }
        )


NODE_MAP = {
    RootNode: ("multi_line_block",),
    UnaryOperatorNode: ("neg_atom",),
    BinaryOperatorNode: ("addition", "subtraction", "multiplication", "division"),
    VariableNode: ("variable", "varname"),
    NumberNode: ("INT", "SIGNED_INT", "FLOAT", "SIGNED_FLOAT", "INDEX"),
}

INV_NODE_MAP = {k: v for v in NODE_MAP for k in NODE_MAP[v]}
