from .ast import (
    StringLiteral,
    NumberLiteral,
    BooleanLiteral,
    Identifier,
    ListLiteral,
    ListAccess,
    FunctionCall,
    VariableAssignment,
    ListAssignment,
    BinaryOperation,
    Comparison,
    LogicalOperation,
    UnaryOperation,
    IfStatement,
    WhileStatement,
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

        if isinstance(statement, ListAssignment):
            return self.execute_list_assignment(statement)

        if isinstance(statement, FunctionCall):
            return self.execute_function_call(statement)

        if isinstance(statement, IfStatement):
            return self.execute_if(statement)

        if isinstance(statement, WhileStatement):
            return self.execute_while(statement)

        raise RuntimeError(
            f"Instruction inconnue : {type(statement).__name__}"
        )

    def execute_assignment(self, statement):
        value = self.evaluate(statement.value)
        self.variables[statement.name] = value

    def execute_list_assignment(self, statement):
        list_value = self.evaluate(statement.list_node)
        index = self.evaluate(statement.index)
        value = self.evaluate(statement.value)

        if not isinstance(list_value, list):
            raise RuntimeError(
                "La valeur ciblée n'est pas une liste"
            )

        if not isinstance(index, int):
            raise RuntimeError(
                "L'index d'une liste doit être un nombre entier"
            )

        try:
            list_value[index] = value
        except IndexError:
            raise RuntimeError(
                f"Index de liste hors limites : {index}"
            )

    def execute_function_call(self, statement):
        if statement.name == "afficher":
            value = self.evaluate(statement.argument)

            if value is True:
                print("vrai")
            elif value is False:
                print("faux")
            else:
                print(value)

            return

        raise RuntimeError(
            f"Fonction inconnue : {statement.name}"
        )

    def execute_if(self, statement):
        condition = self.evaluate(statement.condition)

        if condition:
            for instruction in statement.body:
                self.execute_statement(instruction)

        elif statement.else_body is not None:
            for instruction in statement.else_body:
                self.execute_statement(instruction)

    def execute_while(self, statement):
        while self.evaluate(statement.condition):
            for instruction in statement.body:
                self.execute_statement(instruction)

    def evaluate(self, node):
        if isinstance(node, StringLiteral):
            return node.value

        if isinstance(node, NumberLiteral):
            return node.value

        if isinstance(node, BooleanLiteral):
            return node.value

        if isinstance(node, Identifier):
            if node.name not in self.variables:
                raise RuntimeError(
                    f"Variable inconnue : {node.name}"
                )

            return self.variables[node.name]

        if isinstance(node, ListLiteral):
            return [
                self.evaluate(element)
                for element in node.elements
            ]

        if isinstance(node, ListAccess):
            return self.evaluate_list_access(node)

        if isinstance(node, BinaryOperation):
            return self.evaluate_binary_operation(node)

        if isinstance(node, Comparison):
            return self.evaluate_comparison(node)

        if isinstance(node, LogicalOperation):
            return self.evaluate_logical_operation(node)

        if isinstance(node, UnaryOperation):
            return self.evaluate_unary_operation(node)

        raise RuntimeError(
            f"Expression inconnue : {type(node).__name__}"
        )

    def evaluate_list_access(self, node):
        list_value = self.evaluate(node.list_node)
        index = self.evaluate(node.index)

        if not isinstance(list_value, list):
            raise RuntimeError(
                "La valeur ciblée n'est pas une liste"
            )

        if not isinstance(index, int):
            raise RuntimeError(
                "L'index d'une liste doit être un nombre entier"
            )

        try:
            return list_value[index]
        except IndexError:
            raise RuntimeError(
                f"Index de liste hors limites : {index}"
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
                raise RuntimeError("Division par zéro")

            return left / right

        raise RuntimeError(
            f"Opérateur inconnu : {node.operator}"
        )

    def evaluate_comparison(self, node):
        left = self.evaluate(node.left)
        right = self.evaluate(node.right)

        if node.operator == "==":
            return left == right

        if node.operator == "!=":
            return left != right

        if node.operator == ">":
            return left > right

        if node.operator == "<":
            return left < right

        if node.operator == ">=":
            return left >= right

        if node.operator == "<=":
            return left <= right

        raise RuntimeError(
            f"Comparaison inconnue : {node.operator}"
        )

    def evaluate_logical_operation(self, node):
        left = self.evaluate(node.left)

        if node.operator == "et":
            if not left:
                return False

            return bool(self.evaluate(node.right))

        if node.operator == "ou":
            if left:
                return True

            return bool(self.evaluate(node.right))

        raise RuntimeError(
            f"Opérateur logique inconnu : {node.operator}"
        )

    def evaluate_unary_operation(self, node):
        value = self.evaluate(node.operand)

        if node.operator == "non":
            return not value

        raise RuntimeError(
            f"Opérateur unaire inconnu : {node.operator}"
        )