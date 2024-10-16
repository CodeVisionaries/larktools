from typing import Callable

from lark import Lark

from .ebnf_grammar import grammar
from .tree_utils import (
    is_rule,
    is_terminal,
    get_name,
    get_children,
    get_first_child,
    get_value,
)


class UnaryOperator:
    def __init__(self, func, name):
        self._name = name
        self._func = func

    def __call__(self, node, env):
        child = get_first_child(node)
        assert get_name(child) == self._name

        res = self._func(child, env)
        return res


class BinaryOperator:
    def __init__(self, func, left, right):
        self._left = left
        self._right = right
        self._func = func

    def __call__(self, node, env):
        # is it safe to assume the first child is left?
        child_lhs = get_children(node)[0]
        child_rhs = get_children(node)[1]

        assert get_name(child_lhs) == self._left
        assert get_name(child_rhs) == self._right

        res_lhs = EVAL_MAPPINGS.get(self._left)(
            child_lhs, env
        )
        res_rhs = EVAL_MAPPINGS.get(self._right)(
            child_rhs, env
        )

        return self._func(res_lhs, res_rhs)


class MappedOperator:
    def __init__(self, mappings):
        self._mappings = mappings

    def __call__(self, node, env):
        child = get_first_child(node)
        child_name = get_name(child)

        func = self._mappings.get(child_name)
        # better to raise exception here or have default function?
        assert func is not None

        res = func(child, env)
        return res


def eval_arith_expr(node, env):
    op = UnaryOperator(eval_map, name="sum")
    return op(node, env)


def eval_map(node, env):
    op = MappedOperator(EVAL_MAPPINGS)
    return op(node, env)


def eval_addition(node, env):
    op = BinaryOperator(
        lambda lhs, rhs: lhs + rhs,
        left="sum",
        right="product",
    )
    return op(node, env)


def eval_subtraction(node, env):
    op = BinaryOperator(
        lambda lhs, rhs: lhs - rhs,
        left="sum",
        right="product",
    )
    return op(node, env)


def eval_multiplication(node, env):
    op = BinaryOperator(
        lambda lhs, rhs: lhs * rhs,
        left="product",
        right="atom",
    )
    return op(node, env)


def eval_division(node, env):
    op = BinaryOperator(
        lambda lhs, rhs: lhs / rhs,
        left="product",
        right="atom",
    )
    return op(node, env)


def eval_variable(node, env):
    children = get_children(node)
    assert get_name(children[0]) == "VARNAME"
    varname = get_value(children[0])
    value = env[varname]
    if len(children) > 1:
        for ch in children[1:]:
            assert get_name(ch) == "INDEX"
            idx = int(get_value(ch))
            value = value[idx]
    return value


EVAL_MAPPINGS = {
    "arith_expr": eval_arith_expr,
    "sum": eval_map,
    "product": eval_map,
    "atom": eval_map,
    "addition": eval_addition,
    "subtraction": eval_subtraction,
    "multiplication": eval_multiplication,
    "division": eval_division,
    "INT": lambda child, env: int(get_value(child)),
    "variable": eval_variable,
    "neg_atom": lambda node, env: -eval_map(node, env),
    "bracketed_arith_expr": eval_map,
}
