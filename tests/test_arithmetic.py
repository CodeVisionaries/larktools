import unittest
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


class ArithemticTests(unittest.TestCase):

    def setUp(self):
        self.parser = ArithParser()

    def _parse_and_assert(self, expression: str, expected: Union[int, float]) -> None:
        res = self.parser.parse_and_eval(expression)
        self.assertEqual(expected, res)

    def test_integer_addition(self):
        self._parse_and_assert("3 + 5", 8)
        self._parse_and_assert("5 + 3", 8)
        self._parse_and_assert("9999999999999999 + 555555555555555", 10555555555555554)

    def test_integer_addition_neg(self):
        self._parse_and_assert("-5 + 3", -2)
        self._parse_and_assert("3 + (-5)", -2)
        self._parse_and_assert("9999999999999999 + (-9999999999999999)", 0)

    def test_float_addition(self):
        self._parse_and_assert("3.00000001 + 5.2", 8.20000001)
        self._parse_and_assert("5e3 + 1.23E-2", 5000.00123)


__all__ = ["ArithemticTests"]
