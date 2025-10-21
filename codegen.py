class CodeGen:
    def __init__(self):
        self.instructions = []

    def generate_print(self):
        self.instructions.append('PRINT')

    def generate_store(self, id):
        self.instructions.append(f'STORE {id}')
    
    def generate_load(self, val):
        self.instructions.append(f'LOAD {val}')

    def generate_op(self, op, val):
        if op == '+':
            self.instructions.append(f'ADD {val}')
        if op == '-':
            self.instructions.append(f'SUB {val}')

    def output(self, path = 'out.asm'):
        with open(path, 'w') as f:
            for instr in self.instructions:
                #print(f'writing instr {instr}')
                f.write(instr + '\n')
            print(f'Code generation complete. Output saved to {path}')