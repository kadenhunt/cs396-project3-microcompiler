from lexer import Lexer
from parser import Parser
from codegen import CodeGen  # decoupled later for containerization prep

def main():
    #Lexical Analysis
    lexer = Lexer('source.txt')
    tokens = lexer.tokens()

    #Token Parsing
    parser = Parser(tokens)
    ast = parser.parse_program()

    codegen = CodeGen()
    codegen.generate_program(ast, 'out.asm')
    print("Wrote out.asm")

if __name__ == '__main__':
    main()