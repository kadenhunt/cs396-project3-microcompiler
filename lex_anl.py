class LA:
    def __init__(self, code):
        self.code = code
        self.line_nr = 0
    
    #def raise_error(self, message)

    def tokens(self):
        token_list = []

        for line in self.code.strip().split('\n'):
            self.line_nr += 1
            for token in line.strip().split(' '):
                if token == 'print':
                    token_list.append((token,))
                elif token.isnumeric():
                    token_list.append(('number', int(token)))
                else:
                    print('error')

            token_list.append('\n')

