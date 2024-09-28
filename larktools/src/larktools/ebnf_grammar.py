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

  start: assign_var

  assign_var: VARNAME "=" arith_expr 

  VARNAME: LETTER (LETTER | DIGIT)*

  // Adopted from the calculator example at
  // https://lark-parser.readthedocs.io/en/stable/examples/calc.html 
  // but without the fancy tree shaping directives explained at 
  // https://lark-parser.readthedocs.io/en/stable/tree_construction.html

  arith_expr: sum
  sum: product | addition | subtraction 
  addition: sum "+" product
  subtraction: sum "-" product

  product: atom | multiplication | division
  multiplication: product "*" atom
  division: product "/" atom

  atom: INT | VARNAME | neg_atom | bracketed_arith_expr
  neg_atom: "-" atom
  bracketed_arith_expr: "(" arith_expr ")"

  // The following definitions of terminals are also available
  // in lark/grammars/common.lark and could have been
  // directly imported via the %import statement.

  DIGIT: "0".."9"
  INT: DIGIT+

  LCASE_LETTER: "a".."z"
  UCASE_LETTER: "A".."Z"

  LETTER: UCASE_LETTER | LCASE_LETTER
  WORD: LETTER+

  // Whitespace characters are filtered out before parsing.
  // However, linebreaks are preserved. 

  %import common.WS_INLINE
  %ignore WS_INLINE
"""
