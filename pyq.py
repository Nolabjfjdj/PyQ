import sys

from pyq.lexer import Lexer
from pyq.parser import Parser
from pyq.interpreter import Interpreter, PyQRuntimeError


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

    try:
        run_file(sys.argv[1])

    except SyntaxError as error:
        print(error)
        sys.exit(1)

    except PyQRuntimeError as error:
        line = getattr(error.node, "line", None)

        if line is not None:
            print(
                f"Erreur d'exécution à la ligne {line} : "
                f"{error.message}"
            )
        else:
            print(
                f"Erreur d'exécution : {error.message}"
            )

        sys.exit(1)


if __name__ == "__main__":
    main() 