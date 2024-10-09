import pytest
from typing import Optional, Union

from lark import Lark

from larktools.ebnf_grammar import grammar
from larktools.evaluation import eval_arith_expr


class SyntaxParser:
    def __init__(self):
        self.parser = Lark(grammar, parser="lalr", start="arith_expr")
        self.parse = self.parser.parse

    def parse_and_eval(self, expression: str, env: Optional[Union[None, dict]] = None) -> Union[int, float]:
        tree = self.parse(expression)
        res = eval_arith_expr(tree, {} if env is None else env)
        return res


def _parse_and_assert(expression: str, expected: Union[int, float]) -> None:
    parser = SyntaxParser()
    res = parser.parse_and_eval(expression)
    assert expected == res

def test_multi_line():
    _parse_and_assert("5\n8",8)
    _parse_and_assert("5+5\n3+4\1+2", 3)
