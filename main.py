from lexer import Lexer
from parser import Parser
from codegen import CodeGen

def main():
    #Lexical Analysis
    lexer = Lexer('source.txt')
    tokens = lexer.tokens()

    #CodeGen setup
    codegen = CodeGen()

    #Token Parsing
    parser = Parser(tokens, codegen)
    parser.parse_program()

    #Generate the machine code
    codegen.output()

if __name__ == '__main__':
    main()