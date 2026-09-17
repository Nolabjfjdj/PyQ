import sys

from PYQ.lexer import Lexer
from PYQ.parser import Parser
from PYQ.interpreter import Interpreter


def run_file(filename):
    with open(filename, "r", encoding="utf-8") as file:
        source = file.read()

    lexer = Lexer(source)
    tokens = lexer.tokenize()

    parser = Parser(tokens)
    program = parser.parse()

    interpreter = Interpreter()
    interpreter.execute(program)


def main():
    if len(sys.argv) != 2:
        print("Utilisation : python PYQ.py <fichier.pyQ>")
        sys.exit(1)

    run_file(sys.argv[1])


if __name__ == "__main__":
    main()