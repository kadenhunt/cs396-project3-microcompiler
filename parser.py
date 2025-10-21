from codegen import CodeGen

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
    
    def peek(self):
        # Safe peek: return the next token if it exists, otherwise None
        if self.pos + 1 < len(self.tokens):
            return self.tokens[self.pos + 1]
        return None
               
    def parse_program(self):
        #count = 1
        while not self.at_end():
            #print(f'stmt # {count} ran')
            #count += 1
            if not self.parse_stmt():
                break

    def parse_stmt(self):
        #print(f'starting parse_stmt, token: {self.get_token()[0]}')
        token = self.get_token()
        if token is None:
            return False
        
        if token[0] == 'print':
            #print(f'{token[0]} here is where i call parse_print')
            check = self.parse_print()
            if check:
                if self.get_token()[0]=='newline':
                    self.advance()
                return True
        
        elif token[0] == 'identifier':
            #print(f'{token[0]} here is where i call parse_asmt')
            check = self.parse_asmt()
            if check:
                if self.get_token()[0]=='newline':
                    self.advance()
                return True
        
        else:
            return False
  
    def parse_print(self):
        token = self.get_token()
        
        if token[0] == 'print':
            if self.peek()[0] in ['number', 'identifier']:
                self.advance() #now its on the number or identifier
                check = self.parse_expr()
            else: 
                print('error: expected a value to print')
                return False
            
        else: 
            print('error: expected print statement')
            return False
        
        if check:
            token = self.get_token() #checking to see what the token is after calling expr
            if token and token[0] == 'newline':
                self.codegen.generate_print() #if we are at the end like we should be, print
                return True
            return False
        else: 
            print('error in parse_print')
            return False
    
    def parse_asmt(self):
        token = self.get_token()
        
        if token[0] == 'identifier':
            id = token[1] #save the identifier
            
            if self.peek()[0] == '=':
                self.advance() #now its on =
                
                if self.peek()[0] in ['number', 'identifier']:
                    self.advance() #now its on the number/variable of the expr
                    check = self.parse_expr() #send it to the expr function
                else:
                    print('error: expected a value')
                    return False
                
            else: 
                print('error: expected "="')
                return False
        
        else: 
            print('error: expected variable name')
            return False
        
        if check:
            token = self.get_token() #checking to see what the token is after calling expr
            if token and token[0] == 'newline':
                self.codegen.generate_store(id) #if we are at the end like we should be, store it in the id
                return True
            return False
        else: 
            print('error in parse_asmt')
            return False
    
    def parse_expr(self):
        token = self.get_token()
        
        if token[0] in ['number', 'identifier']:
            self.codegen.generate_load(token[1]) #tell codegen load the number/variable
            token = self.advance() #now we are either on an op or a \n
            
            while token[0] in ['+', '-']: #if its an op
                op = token[0] #save the operator
                token = self.advance() #now the number/variable to be + or -

                if token[0] in ['number', 'identifier']: #ensuring that its a number/variable
                    self.codegen.generate_op(op, token[1]) #tell codegen the op and number/variable
                    token = self.advance()
                else:
                    print('error invalid token')
                    break
            if token[0] == 'newline':
                return True
        else:
            print('error in parse_expr')
            return False
