class Parser:
    def __init__(self, tokens):
        self.tokens = tokens
        self.pos = 0
        
    
    def get_token(self):
        if self.pos < len(self.tokens):
            return self.tokens[self.pos]
        return None
    
    def advance(self):
        # Move the position forward. If there is a next token, return it.
        # If we're at the last token, advance the position to point past
        # the end (len) and return None. This prevents the parser from
        # repeatedly seeing the final token (e.g. a newline) as the
        # current token on subsequent calls.
        if self.pos + 1 < len(self.tokens):
            self.pos += 1
            return self.tokens[self.pos]
        # no next token: move position past the end so get_token() returns None
        self.pos = len(self.tokens)
        return None
    
    def at_end(self):
        return self.pos >= len(self.tokens)
    
    def peek(self):
        # Safe peek: return the next token if it exists, otherwise None
        if self.pos + 1 < len(self.tokens):
            return self.tokens[self.pos + 1]
        return None
               
    def parse_program(self):
        ast = []
        while not self.at_end():
            token = self.get_token()
            if token is None:
                break
            if token[0] == 'newline':
                self.advance()
                continue
            ast.append(self.parse_stmt())
            while self.get_token() and self.get_token()[0] == 'newline':
                self.advance()
        return ('Program', ast)


    def parse_stmt(self):
        token = self.get_token()
        if token is None:
            raise SyntaxError("unexpected EOF in statement")

        if token[0] == 'print':
            return self.parse_print()

        if token[0] == 'identifier':
            return self.parse_asmt()

        raise SyntaxError(f"unexpected token in statement: {token}")


    def parse_print(self):
        t = self.get_token()
        if not t or t[0] != 'print':
            raise SyntaxError("expected 'print'")

        self.advance()  # move past 'print'
        expr = self.parse_expr()
        self.expect_newline()
        return ('Print', expr)

    
    def parse_asmt(self):
        t = self.get_token()
        if not t or t[0] != 'identifier':
            raise SyntaxError("expected identifier at start of assignment")

        name = t[1]
        self.advance()  # past identifier

        eq = self.get_token()
        if not eq or eq[0] != '=':
            raise SyntaxError("expected '=' after identifier")
        self.advance()  # past '='

        expr = self.parse_expr()
        self.expect_newline()
        return ('Assign', name, expr)
    
    def parse_expr(self):
    # first term
        t = self.get_token()
        if not t or t[0] not in ['number', 'identifier']:
            raise SyntaxError("expected number or identifier at start of expression")

        left = ('Number', t[1]) if t[0] == 'number' else ('Var', t[1])
        self.advance()  # move after the first term

        # { ('+'|'-') term }
        t = self.get_token()
        while t and t[0] in ['+', '-']:
            op = t[0]
            self.advance()  # past +/-

            t = self.get_token()
            if not t or t[0] not in ['number', 'identifier']:
                raise SyntaxError("expected number or identifier after operator")
            right = ('Number', t[1]) if t[0] == 'number' else ('Var', t[1])
            self.advance()  # past the right term

            left = ('BinOp', op, left, right)  # left-associative chain
            t = self.get_token()

        return left

    def expect(self, kind, msg):
        t = self.get_token()
        if not t or t[0] != kind:
            got = t[0] if t else 'EOF'
            raise SyntaxError(f"{msg}; got {got}")
        self.advance()
        return t

    def expect_newline(self):
        self.expect('newline', "expected newline at end of statement")
