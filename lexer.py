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
                if token in ['print', '=', '+', '-']:
                    token_list.append((token,))
                elif token.isnumeric():
                    token_list.append(('number', int(token)))
                elif token.isidentifier():
                    token_list.append(('identifier', token))
                else:
                    self.raise_error(f'Syntax Error: Invalid token {token}')

            token_list.append(('newline',))
        
        return token_list