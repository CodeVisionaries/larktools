import pytest
from typing import Optional, Union

from lark import Lark

from larktools.ebnf_grammar import grammar
from larktools.evaluation import eval_multi_line_block


class SyntaxParser:
    def __init__(self):
        self.parser = Lark(grammar, parser="lalr", start="multi_line_block")
        self.parse = self.parser.parse

    def parse_and_eval(self, expression: str, env: Optional[Union[None, dict]] = None) -> Union[int, float]:
        tree = self.parse(expression)
        res = eval_multi_line_block(tree, {} if env is None else env)
        return res


def _parse_and_assert(expression: str, expected: Union[int, float], env: Optional[Union[None, dict]] = None) -> None:
    parser = SyntaxParser()
    res = parser.parse_and_eval(expression, env)
    assert expected == res

def test_multi_line():
    _parse_and_assert("5\n8", 8)
    _parse_and_assert("\n\n\n8", 8)
    _parse_and_assert("8\n\n\n", 8)
    _parse_and_assert("5+5\n3+4\n1+2", 3)
    _parse_and_assert("\n\n5\n\n3\n8", 8)


def test_assignment():
    _parse_and_assert("a=5", 5)
    _parse_and_assert("z=1+2+3", 6)
    _parse_and_assert("y=(1+2+3)", 6)

def test_assignment_env_variable():
    # check env variables is set
    env = {"a":1}
    _parse_and_assert("a=3", 3, env=env)
    assert env["a"] == 3

    _parse_and_assert("y = x + 3", 20, env={"x":17, "i":123})
    _parse_and_assert("y = x + i", 20, env={"x":17, "i":3})

def test_assign_multiline():
    _parse_and_assert("x=3 \n y=4 \n z=x+y",7)
    _parse_and_assert("x=1 \n z = x + y", 3, env={"y":2})



