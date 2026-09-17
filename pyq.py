import sys

from pyq.lexer import Lexer
from pyq.parser import Parser
from pyq.interpreter import Interpreter


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
        print("Utilisation : python pyq.py <fichier.pyq>")
        sys.exit(1)

    run_file(sys.argv[1])


if __name__ == "__main__":
    main()