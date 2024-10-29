import pytest
from typing import Optional, Union

from lark import Lark

from larktools.ebnf_grammar import grammar
from larktools.evaluation import instantiate_eval_tree


class SyntaxParser:
    def __init__(self):
        self.parser = Lark(grammar, parser="lalr", start="multi_line_block")
        self.parse = self.parser.parse

    def parse_and_eval(self, expression: str, env: Optional[Union[None, dict]] = None) -> Union[int, float]:
        tree = self.parse(expression)
        eval_tree = instantiate_eval_tree(tree)
        res = eval_tree({} if env is None else env)
        return res


def _parse_and_assert(expression: str, expected: Union[int, float]) -> None:
    parser = SyntaxParser()
    res = parser.parse_and_eval(expression)
    assert expected == res

def test_multi_line():
    _parse_and_assert("5\n8", 8)
    _parse_and_assert("\n\n\n8", 8)
    _parse_and_assert("8\n\n\n", 8)
    _parse_and_assert("5+5\n3+4\n1+2", 3)
    _parse_and_assert("\n\n5\n\n3\n8", 8)

