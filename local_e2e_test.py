from lexer.service import tokenize
from parser.service import parse
from codegen.service import generate

class B:
    def __init__(self, source):
        self.source = source

# sample source
src = "x = 1 + 2;\nprint x;\n"
print('SOURCE:\n', src)

# tokenize
tok_res = tokenize(B(src))
print('\nTOKENS:\n', tok_res)
if 'error' in tok_res:
    print('lexer error')
    raise SystemExit(1)

toks = tok_res['tokens']

# parse
class Wrap:
    def __init__(self, tokens):
        self.tokens = tokens

parse_res = parse(Wrap(toks))
print('\nAST:\n', parse_res)
if 'error' in parse_res:
    print('parser error')
    raise SystemExit(1)

# codegen
class WrapAST:
    def __init__(self, ast):
        self.ast = ast

gen_res = generate(WrapAST(parse_res['ast']))
print('\nGEN:\n', gen_res)
if 'error' in gen_res:
    print('codegen error')
    raise SystemExit(1)

print('\nMachine code:\n')
print(gen_res.get('machine'))
print('\n--- done ---')
