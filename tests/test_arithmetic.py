import pytest
from typing import Optional, Union

from lark import Lark

from larktools.ebnf_grammar import grammar
from larktools.evaluation import eval_arith_expr


class ArithParser:
    def __init__(self):
        self.parser = Lark(grammar, parser="lalr", start="arith_expr")
        self.parse = self.parser.parse

    def parse_and_eval(self, expression: str, env: Optional[Union[None, dict]] = None) -> Union[int, float]:
        tree = self.parse(expression)
        res = eval_arith_expr(tree, {} if env is None else env)
        return res




def _parse_and_assert(expression: str, expected: Union[int, float]) -> None:
    parser = ArithParser()
    res = parser.parse_and_eval(expression)
    assert expected == res

def _parse_and_assert_collection(tests: list[str, Union[int, float]]) -> None:
    for ipt, expected in tests:
        _parse_and_assert(ipt, expected)

def test_integer_addition():
    _parse_and_assert("3 + 5", 8)
    _parse_and_assert("5 + 3", 8)
    _parse_and_assert("9999999999999999 + 555555555555555", 10555555555555554)

def test_integer_addition_neg():
    _parse_and_assert("-5 + 3", -2)
    _parse_and_assert("3 + (-5)", -2)
    _parse_and_assert("9999999999999999 + (-9999999999999999)", 0)

def test_float_addition() -> None:
    tests = [
        ("3.0 + 5.0", 8),
        ("3.00000001 + 5.2", 8.20000001),
        ("321890.3215687 + 8932.423 + 77231.23", 321890.3215687 + 8932.423 + 77231.23),
    ]
    _parse_and_assert_collection(tests)

def test_float_neg_addition() -> None:
    tests = [
        ("3.0 + -5.0", -2),
        ("-3.00000001 + -5.2", -8.20000001),
        # python issue with brackets - actual result is 390189.12856870005
        ("321890.3215687 + -(8932.423 + (-77231.23))", 321890.3215687 + -(8932.423 + (-77231.23))),
    ]
    _parse_and_assert_collection(tests)

def test_float_subtration() -> None:
    tests = [
        ("3.2 - 5.1", 3.2 - 5.1),
        ("-3.00000001 - 5.2", -3.00000001 - 5.2),
        ("321890.3215687 - 8932.423 - 77231.23", 321890.3215687 - 8932.423 - 77231.23),
    ]
    _parse_and_assert_collection(tests)

def test_scientific_notation_addition() -> None:
    tests = [
        ("5e3 + 1.23E-2", 5000.0123),
        ("1.0267381e+8 + 1.23E-9", 1.0267381e8 + 1.23E-9),
    ]
    _parse_and_assert_collection(tests)

