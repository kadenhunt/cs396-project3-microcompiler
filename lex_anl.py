class Lexer:
    def __init__(self, path):
        self.f = open(path)
        self.line_nr = 0
    
    def raise_error(self, message):
        raise ValueError(f'{self.line_nr}: {message}')

    def tokens(self):
        token_list = []

        for line in self.f:
            self.line_nr += 1
            for token in line.strip().split(' '):
                if token in ['print', '=']:
                    token_list.append((token,))
                elif token.isnumeric():
                    token_list.append(('number', int(token)))
                elif token.isidentifier():
                    token_list.append(('identifier', token))
                else:
                    self.raise_error(f'Syntax Error: Invalid token {token}')

            token_list.append(('newline',))
        
        return token_list
        


class Parser:
    def __init__(self, tokens, codegen):
        self.tokens = tokens
        self.pos = 0
        self.codegen = codegen
    
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
            
    
    def parse_program(self):
        while not self.at_end():
            if not self.parse_stmt():
                break

    def parse_stmt(self):
        token = self.get_token()
        if token is None:
            return False
        
        if token[0] == 'print':
            next_token = self.advance()

            if next_token and next_token[0]=='number':
                self.codegen.generate_print(next_token[1])
                end_token = self.advance()

                if end_token and end_token[0] == 'newline':
                    self.advance()
                    return True
                else: return False
            else:
                print('error expected number after print')
                return False
        
        elif token[0] == 'identifier':
            var = token[1]
            next_token = self.advance()
            if next_token and next_token == '=':
                val = self.advance()
                if val and val[0] == 'number':
                    self.codegen.generate_assign(var, val[1])
                    end_token = self.advance()

                    if end_token and end_token[0]== 'newline':
                        self.advance()
                        return True

        
        else:
            print(f'error token invalid: {token}')
            return False
        
        

        
    



class CodeGen:
    def __init__(self):
        self.instructions = []

    def generate_print(self, value):
        self.instructions.append(f'LOAD {value}')
        self.instructions.append('PRINT')
    
    def generate_assign(self, var, val):
        self.instructions.append(f'LOAD {val}')
        self.instructions.append(f'STORE {var}')

    def output(self, path = 'out.asm'):
        with open(path, 'w') as f:
            for instr in self.instructions:
                f.write(instr + '\n')
            print(f'Code generation complete. Output saved to {path}')


