from .ast import (
    StringLiteral,
    NumberLiteral,
    Identifier,
    FunctionCall,
    VariableAssignment,
    BinaryOperation,
)


class Interpreter:
    def __init__(self):
        self.variables = {}

    def execute(self, program):
        for statement in program.statements:
            self.execute_statement(statement)

    def execute_statement(self, statement):
        if isinstance(statement, VariableAssignment):
            return self.execute_assignment(statement)

        if isinstance(statement, FunctionCall):
            return self.execute_function_call(statement)

        raise RuntimeError(
            f"Instruction inconnue : {type(statement).__name__}"
        )

    def execute_assignment(self, statement):
        value = self.evaluate(statement.value)
        self.variables[statement.name] = value

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

        if isinstance(node, NumberLiteral):
            return node.value

        if isinstance(node, Identifier):
            if node.name not in self.variables:
                raise RuntimeError(
                    f"Variable inconnue : {node.name}"
                )

            return self.variables[node.name]

        if isinstance(node, BinaryOperation):
            return self.evaluate_binary_operation(node)

        raise RuntimeError(
            f"Expression inconnue : {type(node).__name__}"
        )

    def evaluate_binary_operation(self, node):
        left = self.evaluate(node.left)
        right = self.evaluate(node.right)

        if node.operator == "+":
            return left + right

        if node.operator == "-":
            return left - right

        if node.operator == "*":
            return left * right

        if node.operator == "/":
            if right == 0:
                raise RuntimeError(
                    "Division par zéro"
                )

            return left / right

        raise RuntimeError(
            f"Opérateur inconnu : {node.operator}"
        )