from lark import Lark
from .ebnf_grammar import grammar
from .tree_utils import (
    is_rule,
    is_terminal,
    get_name,
    get_children,
    get_value,
)


def eval_arith_expr(node, env):
    child = get_children(node)[0]
    child_name = get_name(child)
    assert child_name == "sum"
    return eval_sum(child, env)


def eval_sum(node, env):
    # we know there is only one child because
    # of formal grammar definition
    child = get_children(node)[0] 
    child_name = get_name(child)
    if child_name == "product":
        return eval_product(child, env)
    elif child_name == "addition":
        return eval_addition(child, env)
    elif child_name == "subtraction":
        return eval_subtraction(child, env)


def eval_product(node, env):
    child = get_children(node)[0]
    child_name = get_name(child)
    if child_name == "atom":
        return eval_atom(child, env)
    elif child_name == "multiplication":
        return eval_multiplication(child, env)
    elif child_name == "division":
        return eval_division(child, env)


def eval_addition(node, env):
    child1 = get_children(node)[0]
    child2 = get_children(node)[1]
    assert get_name(child1) == "sum"
    assert get_name(child2) == "product"
    res1 = eval_sum(child1, env)
    res2 = eval_product(child2, env)
    return res1 + res2


def eval_subtraction(node, env):
    child1 = get_children(node)[0]
    child2 = get_children(node)[1]
    assert get_name(child1) == "sum"
    assert get_name(child2) == "product"
    res1 = eval_sum(child1, env)
    res2 = eval_product(child2, env)
    return res1 - res2


def eval_multiplication(node, env):
    child1 = get_children(node)[0]
    child2 = get_children(node)[1]
    assert get_name(child1) == "product"
    assert get_name(child2) == "atom"
    res1 = eval_product(child1, env)
    res2 = eval_atom(child2, env)
    return res1 * res2


def eval_division(node, env):
    child1 = get_children(node)[0]
    child2 = get_children(node)[1]
    assert get_name(child1) == "product"
    assert get_name(child2) == "atom"
    res1 = eval_product(child1, env)
    res2 = eval_atom(child2, env)
    return res1 / res2


def eval_atom(node, env):
    child = get_children(node)[0]
    child_name = get_name(child)
    if child_name == "INT":
        return int(get_value(child))
    elif child_name == "SIGNED_FLOAT":
        return float(get_value(child))
    elif child_name == "variable":
        return eval_variable(child, env)
    elif child_name == "neg_atom":
        return eval_neg_atom(child, env)
    elif child_name == "bracketed_arith_expr":
        return eval_bracketed_arith_expr(child, env)


def eval_neg_atom(node, env):
    # the "-" character appearing in the production rule is
    # filtered out by lark by default because it is a constant
    # character. Therefore, it doesn't appear among the child nodes
    child = get_children(node)[0]
    assert get_name(child) == "atom"
    return (-eval_atom(child, env))


def eval_bracketed_arith_expr(node, env):
    # same here, the constant characters "(" and ")"
    # are filtered out and don't appear as child nodes
    child = get_children(node)[0]
    assert get_name(child) == "arith_expr"
    return eval_arith_expr(child, env)

def eval_line(node, env):
    # this is the content of a single line of input
    child = get_children(node)[0]
    child_name = get_name(child)
    if child_name == "arith_expr":
        return eval_arith_expr(child, env)

def eval_multi_line_block(node, env):
    # this can be either an arithmetic expression or 
    # composed lines
    children = get_children(node)
    for child in children:
        child_name = get_name(child)
        assert child_name == "line"
        res = eval_line(child, env)
    return res

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
