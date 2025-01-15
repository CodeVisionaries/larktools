import pytest
from typing import Optional, Union

from lark import Lark

from larktools.ebnf_grammar import grammar
from larktools.evaluation import instantiate_eval_tree


class LogicParser:
    def __init__(self):
        self.parser = Lark(grammar, parser="lalr", start="logic_expr")

    def parse_and_eval(self, expression: str, env: Optional[dict] = None) -> Union[int, float]:
        tree = self.parser.parse(expression)
        eval_tree = instantiate_eval_tree(tree)
        res = eval_tree({} if env is None else env)
        return res


def _parse_and_assert(expression: str, expected: Union[int, float], env: Optional[dict] = None) -> None:
    parser = LogicParser()
    res = parser.parse_and_eval(expression, env)
    assert expected == res

def _parse_and_assert_collection(tests: list[str, Union[int, float]]) -> None:
    for ipt, expected in tests:
        _parse_and_assert(ipt, expected)


def test_comparison():
    _parse_and_assert("3 > 5", False)
    _parse_and_assert("3 >= 5", False)
    _parse_and_assert("3 >= 3", True)
    _parse_and_assert("3 >= 3", True)
    _parse_and_assert("5 == 3 + 2", True)
    _parse_and_assert("2 + 3 == 3 + 2", True)
    _parse_and_assert("5 == 3", False)
    _parse_and_assert("3 <= 5", True)
    _parse_and_assert("3 <= 3", True)
    _parse_and_assert("3 <= 2", False)
    _parse_and_assert("3 < 5", True)
    _parse_and_assert("3 != 5", True)
    _parse_and_assert("5 !=  5", False)


def test_logic_states():
    _parse_and_assert("True", True)
    _parse_and_assert("False", False)

def test_logic_operations():
    _parse_and_assert("False or True", True)
    _parse_and_assert("False or False", False)
    _parse_and_assert("True or True", True)
    _parse_and_assert("True or False", True)

    _parse_and_assert("False and True", False)
    _parse_and_assert("False and False", False)
    _parse_and_assert("True and True", True)
    _parse_and_assert("True and False", False)

def test_logic_negation():
    _parse_and_assert("not True", False)
    _parse_and_assert("not False", True)



