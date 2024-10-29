grammar = """

  // see https://lark-parser.readthedocs.io/en/stable/grammar.html 
  // for explanation of EBNF notation.
  // Briefly:
  //
  // *) Rule names are given in lowercase letters, e.g. assign_var below.
  // *) Terminal names are given in uppercase letters, e.g. DIGIT below.
  //
  // A rule is a placeholder for sequences of rules and terminals
  // A terminal is a placeholder for character strings and a terminal definition
  // can only contain characters and other terminal names but must not contain rule names.
  //
  // The top level rule at which the matching/expansion process starts is named "start".

  start: multi_line_block

  variable: VARNAME ("[" INDEX "]")*
  VARNAME: LETTER (LETTER | DIGIT)*
  INDEX: INT

  // Adopted from the calculator example at
  // https://lark-parser.readthedocs.io/en/stable/examples/calc.html 
  // but without the fancy tree shaping directives explained at 
  // https://lark-parser.readthedocs.io/en/stable/tree_construction.html

  
  multi_line_block: (line _NL? | _NL )* 
  line: arith_expr | assignment

  assignment: VARNAME "=" arith_expr

  logic_expr: logic_state | logic_operation | logic_comparison # removing logic_comparison here will make other logic tests succeed.

  logic_state: BOOLEAN

  logic_operation: logic_and | logic_or | logic_not
  logic_and: logic_expr "and" logic_state
  logic_or: logic_expr "or" logic_state
  logic_not: "not" logic_expr

  logic_comparison: logic_greater_than | logic_greater_equal | logic_equal | logic_smaller_equal | logic_smaller_than | logic_unequal
  logic_greater_than: arith_expr ">" arith_expr
  logic_greater_equal: arith_expr ">=" arith_expr
  logic_equal: arith_expr "==" arith_expr
  logic_smaller_equal: arith_expr "<=" arith_expr
  logic_smaller_than: arith_expr "<" arith_expr
  logic_unequal: arith_expr "!=" arith_expr
  
  
  arith_expr: sum
  sum: product | addition | subtraction 
  addition: sum "+" product
  subtraction: sum "-" product

  product: atom | multiplication | division
  multiplication: product "*" atom
  division: product "/" atom

  atom: SIGNED_FLOAT | INT | variable | neg_atom | bracketed_arith_expr
  neg_atom: "-" atom
  bracketed_arith_expr: "(" arith_expr ")"

  // The following definitions of terminals are also available
  // in lark/grammars/common.lark and could have been
  // directly imported via the %import statement.

  DIGIT: "0".."9"
  INT: DIGIT+
  SIGNED_INT: ["+"|"-"] INT
  DECIMAL: INT "." INT? | "." INT


  _EXP: ("e"|"E") SIGNED_INT
  FLOAT: INT _EXP | DECIMAL _EXP?
  SIGNED_FLOAT: ["+"|"-"] FLOAT

  LCASE_LETTER: "a".."z"
  UCASE_LETTER: "A".."Z"

  LETTER: UCASE_LETTER | LCASE_LETTER
  WORD: LETTER+

  BOOLEAN: "True" | "False"

  // Whitespace characters are filtered out before parsing.
  // However, linebreaks are preserved. 

  %import common.WS_INLINE
  %ignore WS_INLINE
  %import common.NEWLINE -> _NL
"""
