from .ast import StringLiteral, FunctionCall


class Interpreter:
    def execute(self, program):
        for statement in program.statements:
            self.execute_statement(statement)

    def execute_statement(self, statement):
        if isinstance(statement, FunctionCall):
            return self.execute_function_call(statement)

        raise RuntimeError(
            f"Instruction inconnue : {type(statement).__name__}"
        )

    def execute_function_call(self, statement):
        if statement.name == "afficher":
            value = self.evaluate(statement.argument)
            print(value)
            return

        raise RuntimeError(
            f"Fonction inconnue : {statement.name}"
        )

    def evaluate(self, node):
        if isinstance(node, StringLiteral):
            return node.value

        raise RuntimeError(
            f"Expression inconnue : {type(node).__name__}"
        )