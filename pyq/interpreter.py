from .ast import (
    StringLiteral,
    NumberLiteral,
    BooleanLiteral,
    NullLiteral,
    Identifier,
    ListLiteral,
    DictLiteral,
    IndexAccess,
    MethodCall,
    FunctionCall,
    VariableAssignment,
    IndexAssignment,
    FunctionDefinition,
    ReturnStatement,
    BinaryOperation,
    Comparison,
    LogicalOperation,
    UnaryOperation,
    IfStatement,
    WhileStatement,
    ForStatement,
    BreakStatement,
    ContinueStatement,
)


class ReturnSignal(Exception):
    def __init__(self, value):
        self.value = value


class BreakSignal(Exception):
    pass


class ContinueSignal(Exception):
    pass


class Interpreter:
    def __init__(self):
        self.variables = {}
        self.functions = {}
        self.local_scopes = []

    def execute(self, program):
        for statement in program.statements:
            if isinstance(statement, FunctionDefinition):
                self.functions[statement.name] = statement

        for statement in program.statements:
            if isinstance(statement, FunctionDefinition):
                continue

            self.execute_statement(statement)

    def execute_statement(self, statement):
        if isinstance(statement, VariableAssignment):
            return self.execute_assignment(statement)

        if isinstance(statement, IndexAssignment):
            return self.execute_index_assignment(statement)

        if isinstance(statement, FunctionCall):
            return self.execute_function_call(statement)

        if isinstance(statement, MethodCall):
            return self.evaluate(statement)

        if isinstance(statement, FunctionDefinition):
            self.functions[statement.name] = statement
            return

        if isinstance(statement, ReturnStatement):
            if not self.local_scopes:
                raise RuntimeError(
                    "'retourner' ne peut être utilisé qu'à l'intérieur d'une fonction"
                )

            value = None

            if statement.value is not None:
                value = self.evaluate(statement.value)

            raise ReturnSignal(value)

        if isinstance(statement, BreakStatement):
            raise BreakSignal()

        if isinstance(statement, ContinueStatement):
            raise ContinueSignal()

        if isinstance(statement, IfStatement):
            return self.execute_if(statement)

        if isinstance(statement, WhileStatement):
            return self.execute_while(statement)

        if isinstance(statement, ForStatement):
            return self.execute_for(statement)

        raise RuntimeError(
            f"Instruction inconnue : {type(statement).__name__}"
        )

    def execute_assignment(self, statement):
        value = self.evaluate(statement.value)

        if self.local_scopes:
            self.local_scopes[-1][statement.name] = value
        else:
            self.variables[statement.name] = value

    def execute_index_assignment(self, statement):
        target = self.evaluate(statement.target)
        index = self.evaluate(statement.index)
        value = self.evaluate(statement.value)

        if isinstance(target, list):
            if not isinstance(index, int):
                raise RuntimeError(
                    "L'index d'une liste doit être un nombre entier"
                )

            try:
                target[index] = value
            except IndexError:
                raise RuntimeError(
                    f"Index de liste hors limites : {index}"
                )

            return

        if isinstance(target, dict):
            try:
                target[index] = value
            except TypeError:
                raise RuntimeError(
                    "La clé du dictionnaire n'est pas valide"
                )

            return

        raise RuntimeError(
            "La valeur ciblée n'est ni une liste ni un dictionnaire"
        )

    def execute_function_call(self, statement):
        if statement.name == "afficher":
            if len(statement.arguments) != 1:
                raise RuntimeError(
                    "afficher() attend exactement un argument"
                )

            value = self.evaluate(statement.arguments[0])

            self.print_value(value)

            return None

        return self.call_function(
            statement.name,
            statement.arguments
        )

    def call_function(self, name, arguments):
        if name not in self.functions:
            raise RuntimeError(
                f"Fonction inconnue : {name}"
            )

        function = self.functions[name]

        if len(arguments) != len(function.parameters):
            raise RuntimeError(
                f"La fonction {name}() attend "
                f"{len(function.parameters)} argument(s), "
                f"mais {len(arguments)} ont été fournis"
            )

        values = [
            self.evaluate(argument)
            for argument in arguments
        ]

        local_scope = {}

        for parameter, value in zip(
            function.parameters,
            values
        ):
            local_scope[parameter] = value

        self.local_scopes.append(local_scope)

        try:
            for statement in function.body:
                self.execute_statement(statement)

        except ReturnSignal as signal:
            return signal.value

        finally:
            self.local_scopes.pop()

        return None

    def print_value(self, value):
        if value is True:
            print("vrai")

        elif value is False:
            print("faux")

        elif value is None:
            print("nul")

        else:
            print(value)

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
            try:
                for instruction in statement.body:
                    self.execute_statement(instruction)

            except ContinueSignal:
                continue

            except BreakSignal:
                break

    def execute_for(self, statement):
        iterable = self.evaluate(statement.iterable)

        if not isinstance(iterable, list):
            raise RuntimeError(
                "La valeur parcourue par 'pour' doit être une liste"
            )

        for value in iterable:
            if self.local_scopes:
                self.local_scopes[-1][statement.variable] = value
            else:
                self.variables[statement.variable] = value

            try:
                for instruction in statement.body:
                    self.execute_statement(instruction)

            except ContinueSignal:
                continue

            except BreakSignal:
                break

    def evaluate(self, node):
        if isinstance(node, StringLiteral):
            return node.value

        if isinstance(node, NumberLiteral):
            return node.value

        if isinstance(node, BooleanLiteral):
            return node.value

        if isinstance(node, NullLiteral):
            return None

        if isinstance(node, Identifier):
            return self.get_variable(node.name)

        if isinstance(node, ListLiteral):
            return [
                self.evaluate(element)
                for element in node.elements
            ]

        if isinstance(node, DictLiteral):
            return self.evaluate_dict_literal(node)

        if isinstance(node, IndexAccess):
            return self.evaluate_index_access(node)

        if isinstance(node, MethodCall):
            return self.execute_method_call(node)

        if isinstance(node, FunctionCall):
            return self.call_function(
                node.name,
                node.arguments
            )

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

    def get_variable(self, name):
        if self.local_scopes:
            local_scope = self.local_scopes[-1]

            if name in local_scope:
                return local_scope[name]

        if name in self.variables:
            return self.variables[name]

        raise RuntimeError(
            f"Variable inconnue : {name}"
        )

    def evaluate_dict_literal(self, node):
        result = {}

        for key_node, value_node in node.entries:
            key = self.evaluate(key_node)
            value = self.evaluate(value_node)

            try:
                result[key] = value
            except TypeError:
                raise RuntimeError(
                    "La clé du dictionnaire n'est pas valide"
                )

        return result

    def evaluate_index_access(self, node):
        target = self.evaluate(node.target)
        index = self.evaluate(node.index)

        if isinstance(target, list):
            if not isinstance(index, int):
                raise RuntimeError(
                    "L'index d'une liste doit être un nombre entier"
                )

            try:
                return target[index]
            except IndexError:
                raise RuntimeError(
                    f"Index de liste hors limites : {index}"
                )

        if isinstance(target, dict):
            try:
                return target[index]
            except KeyError:
                raise RuntimeError(
                    f"Clé de dictionnaire inconnue : {index}"
                )
            except TypeError:
                raise RuntimeError(
                    "La clé du dictionnaire n'est pas valide"
                )

        if isinstance(target, str):
            if not isinstance(index, int):
                raise RuntimeError(
                    "L'index d'une chaîne doit être un nombre entier"
                )

            try:
                return target[index]
            except IndexError:
                raise RuntimeError(
                    f"Index de chaîne hors limites : {index}"
                )

        raise RuntimeError(
            "La valeur ciblée ne peut pas être indexée"
        )

    def execute_method_call(self, node):
        target = self.evaluate(node.target)

        if isinstance(target, list):
            if node.name == "ajouter":
                if len(node.arguments) != 1:
                    raise RuntimeError(
                        "ajouter() attend exactement un argument"
                    )

                value = self.evaluate(node.arguments[0])
                target.append(value)

                return None

            if node.name == "retirer":
                if len(node.arguments) != 1:
                    raise RuntimeError(
                        "retirer() attend exactement un argument"
                    )

                value = self.evaluate(node.arguments[0])

                try:
                    target.remove(value)
                except ValueError:
                    raise RuntimeError(
                        f"Valeur absente de la liste : {value}"
                    )

                return None

            if node.name == "taille":
                if len(node.arguments) != 0:
                    raise RuntimeError(
                        "taille() n'attend aucun argument"
                    )

                return len(target)

            raise RuntimeError(
                f"Méthode de liste inconnue : {node.name}"
            )

        if isinstance(target, str):
            if node.name == "taille":
                if len(node.arguments) != 0:
                    raise RuntimeError(
                        "taille() n'attend aucun argument"
                    )

                return len(target)

            if node.name == "contient":
                if len(node.arguments) != 1:
                    raise RuntimeError(
                        "contient() attend exactement un argument"
                    )

                value = self.evaluate(node.arguments[0])

                if not isinstance(value, str):
                    raise RuntimeError(
                        "contient() attend une chaîne de caractères"
                    )

                return value in target

            if node.name == "commence_par":
                if len(node.arguments) != 1:
                    raise RuntimeError(
                        "commence_par() attend exactement un argument"
                    )

                value = self.evaluate(node.arguments[0])

                if not isinstance(value, str):
                    raise RuntimeError(
                        "commence_par() attend une chaîne de caractères"
                    )

                return target.startswith(value)

            if node.name == "finit_par":
                if len(node.arguments) != 1:
                    raise RuntimeError(
                        "finit_par() attend exactement un argument"
                    )

                value = self.evaluate(node.arguments[0])

                if not isinstance(value, str):
                    raise RuntimeError(
                        "finit_par() attend une chaîne de caractères"
                    )

                return target.endswith(value)

            raise RuntimeError(
                f"Méthode de chaîne inconnue : {node.name}"
            )

        raise RuntimeError(
            f"Les méthodes ne sont pas disponibles pour cette valeur"
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

            return bool(
                self.evaluate(node.right)
            )

        if node.operator == "ou":
            if left:
                return True

            return bool(
                self.evaluate(node.right)
            )

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