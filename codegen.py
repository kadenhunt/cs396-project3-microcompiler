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

        # Walk the AST produced by Parser and emit instructions, then write the file.
    def generate_program(self, ast, out_path='out.asm'):
        """
        ast = ('Program', [stmt, ...])
        stmt = ('Assign', name, expr) | ('Print', expr)
        expr = ('Number', n) | ('Var', name) | ('BinOp', op, left, right)
        """
        tag, stmts = ast
        assert tag == 'Program', f"expected Program node, got {tag}"

        for s in stmts:
            if s[0] == 'Assign':
                _, name, expr = s
                self._gen_expr(expr)
                self.generate_store(name)
            elif s[0] == 'Print':
                _, expr = s
                self._gen_expr(expr)
                self.generate_print()
            else:
                raise RuntimeError(f"unknown statement node: {s[0]}")

        # finally write the file
        self.output(out_path)

    def _gen_expr(self, node):
        t = node[0]
        if t == 'Number':
            _, n = node
            self.generate_load(n)
            return
        if t == 'Var':
            _, name = node
            self.generate_load(name)
            return
        if t == 'BinOp':
            _, _, base, _ = node
            base_term, rest_ops = self._flatten_add_sub(node)

            # load the first/base term
            if base_term[0] == 'Number':
                self.generate_load(base_term[1])
            elif base_term[0] == 'Var':
                self.generate_load(base_term[1])
            else:
                # shouldn't happen for our current grammar
                self._gen_expr(base_term)

            # then apply each + / - with its term
            for op_sym, term in rest_ops:
                if term[0] == 'Number':
                    self.generate_op(op_sym, term[1])
                elif term[0] == 'Var':
                    self.generate_op(op_sym, term[1])
                else:
                    # fallback (not expected in current scope)
                    raise RuntimeError(f"unsupported term in BinOp: {term}")
            return

        raise RuntimeError(f"unknown expr node: {t}")

    def _flatten_add_sub(self, node):
        """
        Convert a left-associative chain of +/-
        Example:
          ('BinOp','-', ('BinOp','+', A, B), C)
        becomes:
          base = A
          ops  = [('+', B), ('-', C)]
        """
        ops = []
        cur = node
        # walk down the left spine
        while cur[0] == 'BinOp' and cur[2][0] == 'BinOp':
            ops.append((cur[1], cur[3]))  # (op, right)
            cur = cur[2]                  # go left
        # now cur is either BinOp(base,right) or base
        if cur[0] == 'BinOp':
            base = cur[2]
            ops.append((cur[1], cur[3]))
        else:
            base = cur
        # we collected from top to bottom; reverse to get left-to-right order
        ops.reverse()
        return base, ops
