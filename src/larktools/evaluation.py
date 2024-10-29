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
    elif child_name == "assignment":
        return eval_assignment(child, env)

def eval_multi_line_block(node, env):
    # this can be either an arithmetic expression or 
    # composed lines
    children = get_children(node)
    for child in children:
        child_name = get_name(child)
        assert child_name == "line"
        res = eval_line(child, env)
    return res


def eval_assignment(node, env):
    # assign result of an expression to a variable
    child1, child2 = get_children(node)[0:2]
    assert get_name(child1) == "VARNAME"
    assert get_name(child2) == "arith_expr"

    varname = get_value(child1)
    env[varname] = eval_arith_expr(child2, env)
    return env[varname]


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

def eval_logic_expr(node, env):
    child = get_children(node)[0]
    child_name = get_name(child)
    if child_name == 'logic_state':
        return eval_logic_state(child, env)
    if child_name == 'logic_operation':
        return eval_logic_operation(child, env)
    if child_name == 'logic_comparison':
        return eval_logic_comparison(child, env)
    raise ValueError('Unexpected child name')

def eval_logic_state(node,env):
    child = get_children(node)[0]
    child_name = get_name(child)
    if child_name == 'BOOLEAN':
        value = get_value(child)
        if value == 'True':
            return True
        if value == 'False':
            return False
    if child_name == 'variable':
        return eval_variable(child, env)
    
def eval_logic_operation(node, env):
    child = get_children(node)[0]
    child_name = get_name(child)
    if child_name == 'logic_and':
        return eval_logic_and(child, env)
    if child_name == 'logic_or':
        return eval_logic_or(child, env)
    if child_name == 'logic_not':
        return eval_logic_not(child, env)

def eval_logic_and(node, env):
    child1, child2 = get_children(node)
    assert get_name(child1) == 'logic_expr'
    assert get_name(child2) == 'logic_state'

    return eval_logic_expr(child1, env) & eval_logic_state(child2, env)

def eval_logic_or(node, env):
    child1, child2 = get_children(node)
    assert get_name(child1) == 'logic_expr'
    assert get_name(child2) == 'logic_state'

    return eval_logic_expr(child1, env) | eval_logic_state(child2, env)

def eval_logic_not(node, env):
    child = get_children(node)[0]
    assert get_name(child) == 'logic_expr'

    return not eval_logic_expr(child, env)

def eval_logic_comparison(node, env):
    child = get_children(node)[0]
    child_name = get_name(child)

    if child_name == 'logic_greater_than':
        return eval_logic_greater_than(child, env)
    if child_name == 'logic_greater_equal':
        return eval_logic_greater_equal(child, env)
    if child_name == 'logic_equal':
        return eval_logic_equal(child, env)
    if child_name == 'logic_smaller_equal':
        return eval_logic_smaller_equal(child, env)
    if child_name == 'logic_smaller_than':
        return eval_logic_smaller_than(child, env)
    if child_name == 'logic_unequal':
        return eval_logic_unequal(child, env)
    
def eval_logic_greater_than(node, env):
    child1, child2 = get_children(node)
    assert get_name(child1) == 'arith_expr'
    assert get_name(child2) == 'arith_expr'

    return eval_arith_expr(child1, env) > eval_arith_expr(child2, env)

    
def eval_logic_greater_equal(node, env):
    child1, child2 = get_children(node)
    assert get_name(child1) == 'arith_expr'
    assert get_name(child2) == 'arith_expr'

    return eval_arith_expr(child1, env) >= eval_arith_expr(child2, env)

    
def eval_logic_equal(node, env):
    child1, child2 = get_children(node)
    assert get_name(child1) == 'arith_expr'
    assert get_name(child2) == 'arith_expr'

    return eval_arith_expr(child1, env) == eval_arith_expr(child2, env)
    
def eval_logic_smaller_equal(node, env):
    child1, child2 = get_children(node)
    assert get_name(child1) == 'arith_expr'
    assert get_name(child2) == 'arith_expr'

    return eval_arith_expr(child1, env) <= eval_arith_expr(child2, env)

def eval_logic_smaller_than(node, env):
    child1, child2 = get_children(node)
    assert get_name(child1) == 'arith_expr'
    assert get_name(child2) == 'arith_expr'

    return eval_arith_expr(child1, env) <= eval_arith_expr(child2, env)
    
def eval_logic_unequal(node, env):
    child1, child2 = get_children(node)
    assert get_name(child1) == 'arith_expr'
    assert get_name(child2) == 'arith_expr'

    return eval_arith_expr(child1, env) != eval_arith_expr(child2, env)
