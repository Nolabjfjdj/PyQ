from .ast import (
    Program,
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


class PyQRuntimeError(Exception):
    def __init__(self, message, node=None):
        self.message = message
        self.node = node
        super().__init__(message)


class ReturnSignal(Exception):
    def __init__(self, value):
        self.value = value


class BreakSignal(Exception):
    pass


class ContinueSignal(Exception):
    pass


class Function:
    def __init__(self, definition):
        self.definition = definition


class Environment:
    def __init__(self, parent=None):
        self.values = {}
        self.parent = parent

    def define(self, name, value):
        self.values[name] = value

    def get(self, name):
        if name in self.values:
            return self.values[name]

        if self.parent is not None:
            return self.parent.get(name)

        raise KeyError(name)

    def set(self, name, value):
        if name in self.values:
            self.values[name] = value
            return

        if self.parent is not None:
            try:
                self.parent.set(name, value)
                return
            except KeyError:
                pass

        self.values[name] = value


class Interpreter:
    def __init__(self):
        self.environment = Environment()

    def execute(self, node):
        method = getattr(
            self,
            f"execute_{type(node).__name__}",
            None
        )

        if method is None:
            raise PyQRuntimeError(
                f"Instruction non supportée : {type(node).__name__}",
                node
            )

        return method(node)

    def execute_Program(self, node):
        result = None

        for statement in node.statements:
            result = self.execute(statement)

        return result

    def execute_StringLiteral(self, node):
        return node.value

    def execute_NumberLiteral(self, node):
        return node.value

    def execute_BooleanLiteral(self, node):
        return node.value

    def execute_NullLiteral(self, node):
        return None

    def execute_Identifier(self, node):
        try:
            return self.environment.get(node.name)
        except KeyError:
            raise PyQRuntimeError(
                f"Variable inconnue : {node.name}",
                node
            )

    def execute_ListLiteral(self, node):
        return [
            self.execute(element)
            for element in node.elements
        ]

    def execute_DictLiteral(self, node):
        result = {}

        for key_node, value_node in node.entries:
            key = self.execute(key_node)
            value = self.execute(value_node)
            result[key] = value

        return result

    def execute_IndexAccess(self, node):
        target = self.execute(node.target)
        index = self.execute(node.index)

        try:
            return target[index]
        except (IndexError, KeyError, TypeError):
            if isinstance(target, str):
                raise PyQRuntimeError(
                    f"Index de chaîne hors limites : {index}",
                    node
                )

            if isinstance(target, list):
                raise PyQRuntimeError(
                    f"Index de liste hors limites : {index}",
                    node
                )

            if isinstance(target, dict):
                raise PyQRuntimeError(
                    f"Clé de dictionnaire inexistante : {index}",
                    node
                )

            raise PyQRuntimeError(
                "Indexation impossible sur cette valeur",
                node
            )

    def execute_MethodCall(self, node):
        target = self.execute(node.target)
        arguments = [
            self.execute(argument)
            for argument in node.arguments
        ]

        if isinstance(target, list):
            if node.name == "taille":
                if len(arguments) != 0:
                    raise PyQRuntimeError(
                        "taille() n'attend aucun argument",
                        node
                    )

                return len(target)

            if node.name == "ajouter":
                if len(arguments) != 1:
                    raise PyQRuntimeError(
                        "ajouter() attend exactement un argument",
                        node
                    )

                target.append(arguments[0])
                return None

            if node.name == "retirer":
                if len(arguments) != 1:
                    raise PyQRuntimeError(
                        "retirer() attend exactement un argument",
                        node
                    )

                try:
                    target.remove(arguments[0])
                except ValueError:
                    raise PyQRuntimeError(
                        f"Valeur introuvable dans la liste : {arguments[0]}",
                        node
                    )

                return None

            raise PyQRuntimeError(
                f"Méthode de liste inconnue : {node.name}",
                node
            )

        if isinstance(target, str):
            if node.name == "taille":
                if len(arguments) != 0:
                    raise PyQRuntimeError(
                        "taille() n'attend aucun argument",
                        node
                    )

                return len(target)

            if node.name == "contient":
                if len(arguments) != 1:
                    raise PyQRuntimeError(
                        "contient() attend exactement un argument",
                        node
                    )

                return arguments[0] in target

            if node.name == "commence_par":
                if len(arguments) != 1:
                    raise PyQRuntimeError(
                        "commence_par() attend exactement un argument",
                        node
                    )

                return target.startswith(arguments[0])

            if node.name == "finit_par":
                if len(arguments) != 1:
                    raise PyQRuntimeError(
                        "finit_par() attend exactement un argument",
                        node
                    )

                return target.endswith(arguments[0])

            if node.name == "majuscule":
                if len(arguments) != 0:
                    raise PyQRuntimeError(
                        "majuscule() n'attend aucun argument",
                        node
                    )

                return target.upper()

            if node.name == "minuscule":
                if len(arguments) != 0:
                    raise PyQRuntimeError(
                        "minuscule() n'attend aucun argument",
                        node
                    )

                return target.lower()

            if node.name == "remplacer":
                if len(arguments) != 2:
                    raise PyQRuntimeError(
                        "remplacer() attend exactement deux arguments",
                        node
                    )

                return target.replace(
                    arguments[0],
                    arguments[1]
                )

            if node.name == "separer":
                if len(arguments) != 1:
                    raise PyQRuntimeError(
                        "separer() attend exactement un argument",
                        node
                    )

                return target.split(arguments[0])

            raise PyQRuntimeError(
                f"Méthode de chaîne inconnue : {node.name}",
                node
            )

        raise PyQRuntimeError(
            f"La méthode '{node.name}' n'est pas disponible sur cette valeur",
            node
        )

    def execute_FunctionCall(self, node):
        if node.name == "afficher":
            if len(node.arguments) != 1:
                raise PyQRuntimeError(
                    "afficher() attend exactement un argument",
                    node
                )

            value = self.execute(node.arguments[0])
            print(self.print_value(value))
            return None

        try:
            function = self.environment.get(node.name)
        except KeyError:
            raise PyQRuntimeError(
                f"Fonction inconnue : {node.name}",
                node
            )

        if not isinstance(function, Function):
            raise PyQRuntimeError(
                f"'{node.name}' n'est pas une fonction",
                node
            )

        if len(node.arguments) != len(function.definition.parameters):
            raise PyQRuntimeError(
                f"La fonction '{node.name}' attend "
                f"{len(function.definition.parameters)} argument(s)",
                node
            )

        values = [
            self.execute(argument)
            for argument in node.arguments
        ]

        previous_environment = self.environment

        local_environment = Environment(
            parent=previous_environment
        )

        for parameter, value in zip(
            function.definition.parameters,
            values
        ):
            local_environment.define(parameter, value)

        self.environment = local_environment

        try:
            for statement in function.definition.body:
                self.execute(statement)

        except ReturnSignal as signal:
            return signal.value

        finally:
            self.environment = previous_environment

        return None

    def execute_VariableAssignment(self, node):
        value = self.execute(node.value)
        self.environment.set(node.name, value)
        return value

    def execute_IndexAssignment(self, node):
        target = self.execute(node.target)
        index = self.execute(node.index)
        value = self.execute(node.value)

        try:
            target[index] = value
        except (IndexError, KeyError, TypeError):
            if isinstance(target, list):
                raise PyQRuntimeError(
                    f"Index de liste hors limites : {index}",
                    node
                )

            if isinstance(target, dict):
                raise PyQRuntimeError(
                    f"Impossible de modifier la clé : {index}",
                    node
                )

            raise PyQRuntimeError(
                "Modification par index impossible sur cette valeur",
                node
            )

        return value

    def execute_FunctionDefinition(self, node):
        self.environment.define(
            node.name,
            Function(node)
        )

        return None

    def execute_ReturnStatement(self, node):
        if node.value is None:
            raise ReturnSignal(None)

        value = self.execute(node.value)

        raise ReturnSignal(value)

    def execute_BinaryOperation(self, node):
        left = self.execute(node.left)
        right = self.execute(node.right)

        try:
            if node.operator == "+":
                return left + right

            if node.operator == "-":
                return left - right

            if node.operator == "*":
                return left * right

            if node.operator == "/":
                return left / right

        except (TypeError, ZeroDivisionError) as error:
            if isinstance(error, ZeroDivisionError):
                raise PyQRuntimeError(
                    "Division par zéro",
                    node
                )

            raise PyQRuntimeError(
                "Opération impossible entre ces valeurs",
                node
            )

        raise PyQRuntimeError(
            f"Opérateur inconnu : {node.operator}",
            node
        )

    def execute_Comparison(self, node):
        left = self.execute(node.left)
        right = self.execute(node.right)

        try:
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

        except TypeError:
            raise PyQRuntimeError(
                "Comparaison impossible entre ces valeurs",
                node
            )

        raise PyQRuntimeError(
            f"Opérateur de comparaison inconnu : {node.operator}",
            node
        )

    def execute_LogicalOperation(self, node):
        left = self.execute(node.left)

        if node.operator == "et":
            if not self.is_truthy(left):
                return False

            right = self.execute(node.right)
            return self.is_truthy(right)

        if node.operator == "ou":
            if self.is_truthy(left):
                return True

            right = self.execute(node.right)
            return self.is_truthy(right)

        raise PyQRuntimeError(
            f"Opérateur logique inconnu : {node.operator}",
            node
        )

    def execute_UnaryOperation(self, node):
        operand = self.execute(node.operand)

        if node.operator == "non":
            return not self.is_truthy(operand)

        raise PyQRuntimeError(
            f"Opérateur unaire inconnu : {node.operator}",
            node
        )

    def execute_IfStatement(self, node):
        if self.is_truthy(self.execute(node.condition)):
            for statement in node.body:
                self.execute(statement)

        elif node.else_body is not None:
            for statement in node.else_body:
                self.execute(statement)

        return None

    def execute_WhileStatement(self, node):
        while self.is_truthy(self.execute(node.condition)):
            try:
                for statement in node.body:
                    self.execute(statement)

            except BreakSignal:
                break

            except ContinueSignal:
                continue

        return None

    def execute_ForStatement(self, node):
        iterable = self.execute(node.iterable)

        try:
            iterator = iter(iterable)
        except TypeError:
            raise PyQRuntimeError(
                "La valeur utilisée dans 'pour' n'est pas itérable",
                node
            )

        for value in iterator:
            self.environment.set(
                node.variable,
                value
            )

            try:
                for statement in node.body:
                    self.execute(statement)

            except BreakSignal:
                break

            except ContinueSignal:
                continue

        return None

    def execute_BreakStatement(self, node):
        raise BreakSignal()

    def execute_ContinueStatement(self, node):
        raise ContinueSignal()

    def is_truthy(self, value):
        return bool(value)

    def print_value(self, value):
        if value is True:
            return "vrai"

        if value is False:
            return "faux"

        if value is None:
            return "nul"

        if isinstance(value, list):
            return "[" + ", ".join(
                self.print_value(item)
                for item in value
            ) + "]"

        if isinstance(value, dict):
            entries = []

            for key, item in value.items():
                entries.append(
                    f"{self.print_value(key)}: {self.print_value(item)}"
                )

            return "{" + ", ".join(entries) + "}"

        return str(value)