from lark import Lark
from larktools.ebnf_grammar import grammar
from larktools.evaluation import eval_arith_expr


# initialize the parser with the formal grammar 
parser = Lark(grammar, parser="lalr", start="arith_expr")
parsefun = parser.parse

# generate the parse tree for an arithmetic expression 
arith_expr1 = "3 + (3 - 4/2) * 5"
tree1 = parsefun(arith_expr1)
res1 = eval_arith_expr(tree1, {})
print(f"{arith_expr1} evaluates to {res1}") 

# now with a variable

arith_expr2 = "3 + x*x / 5"
tree2 = parsefun(arith_expr2)
env = {"x": 10}
res2 = eval_arith_expr(tree2, env)
var_assign_str = ", ".join(f"{var}={val}" for var, val in env.items())
print(f"{arith_expr2} evaluates to {res2} when using {var_assign_str}") 
