from pyq.ast import (
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
    ContinueStatement
)


class PyQRuntimeError(Exception):
    def __init__(self, message, node=None):
        super().__init__(message)
        self.message = message
        self.node = node


class ReturnSignal(Exception):
    def __init__(self, value):
        self.value = value


class BreakSignal(Exception):
    pass


class ContinueSignal(Exception):
    pass


class Function:
    def __init__(self, name, parameters, body, closure):
        self.name = name
        self.parameters = parameters
        self.body = body
        self.closure = closure


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
        method_name = f"execute_{type(node).__name__}"
        method = getattr(self, method_name, None)

        if method is None:
            raise PyQRuntimeError(
                f"Instruction non prise en charge : {type(node).__name__}",
                node
            )

        try:
            return method(node)

        except PyQRuntimeError:
            raise

        except KeyError as error:
            raise PyQRuntimeError(
                f"Nom inconnu : {error.args[0]}",
                node
            )

        except ZeroDivisionError:
            raise PyQRuntimeError(
                "Division par zéro",
                node
            )

        except TypeError as error:
            raise PyQRuntimeError(
                f"Opération invalide : {error}",
                node
            )

        except IndexError:
            raise PyQRuntimeError(
                "Index hors limites",
                node
            )

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
                f"Nom inconnu : {node.name}",
                node
            )

    def execute_ListLiteral(self, node):
        return [
            self.execute(element)
            for element in node.elements
        ]

    def execute_DictLiteral(self, node):
        result = {}

        for key, value in node.entries:
            evaluated_key = self.execute(key)
            evaluated_value = self.execute(value)

            try:
                result[evaluated_key] = evaluated_value

            except TypeError:
                raise PyQRuntimeError(
                    "Clé de dictionnaire invalide",
                    node
                )

        return result

    def execute_IndexAccess(self, node):
        target = self.execute(node.target)
        index = self.execute(node.index)

        if isinstance(target, str):
            if not isinstance(index, int):
                raise PyQRuntimeError(
                    "L'index d'une chaîne doit être un entier",
                    node
                )

            if index < 0 or index >= len(target):
                raise PyQRuntimeError(
                    f"Index de chaîne hors limites : {index}",
                    node
                )

            return target[index]

        if isinstance(target, list):
            if not isinstance(index, int):
                raise PyQRuntimeError(
                    "L'index d'une liste doit être un entier",
                    node
                )

            if index < 0 or index >= len(target):
                raise PyQRuntimeError(
                    f"Index de liste hors limites : {index}",
                    node
                )

            return target[index]

        if isinstance(target, dict):
            if index not in target:
                raise PyQRuntimeError(
                    f"Clé absente du dictionnaire : {index}",
                    node
                )

            return target[index]

        raise PyQRuntimeError(
            "Cet élément ne peut pas être indexé",
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
                        f"Élément absent de la liste : {arguments[0]}",
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

                if not isinstance(arguments[0], str):
                    raise PyQRuntimeError(
                        "contient() attend une chaîne",
                        node
                    )

                return arguments[0] in target

            if node.name == "commence_par":
                if len(arguments) != 1:
                    raise PyQRuntimeError(
                        "commence_par() attend exactement un argument",
                        node
                    )

                if not isinstance(arguments[0], str):
                    raise PyQRuntimeError(
                        "commence_par() attend une chaîne",
                        node
                    )

                return target.startswith(arguments[0])

            if node.name == "finit_par":
                if len(arguments) != 1:
                    raise PyQRuntimeError(
                        "finit_par() attend exactement un argument",
                        node
                    )

                if not isinstance(arguments[0], str):
                    raise PyQRuntimeError(
                        "finit_par() attend une chaîne",
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

                if not isinstance(arguments[0], str):
                    raise PyQRuntimeError(
                        "remplacer() attend une chaîne comme premier argument",
                        node
                    )

                if not isinstance(arguments[1], str):
                    raise PyQRuntimeError(
                        "remplacer() attend une chaîne comme deuxième argument",
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

                if not isinstance(arguments[0], str):
                    raise PyQRuntimeError(
                        "separer() attend une chaîne",
                        node
                    )

                return target.split(arguments[0])

            if node.name == "joindre":
                if len(arguments) != 1:
                    raise PyQRuntimeError(
                        "joindre() attend exactement un argument",
                        node
                    )

                if not isinstance(arguments[0], list):
                    raise PyQRuntimeError(
                        "joindre() attend une liste",
                        node
                    )

                if not all(
                    isinstance(item, str)
                    for item in arguments[0]
                ):
                    raise PyQRuntimeError(
                        "joindre() ne peut joindre que des chaînes",
                        node
                    )

                return target.join(arguments[0])

            if node.name == "rogner":
                if len(arguments) > 1:
                    raise PyQRuntimeError(
                        "rogner() attend zéro ou un argument",
                        node
                    )

                if len(arguments) == 0:
                    return target.strip()

                if not isinstance(arguments[0], str):
                    raise PyQRuntimeError(
                        "rogner() attend une chaîne",
                        node
                    )

                return target.strip(arguments[0])

            if node.name == "chercher":
                if len(arguments) != 1:
                    raise PyQRuntimeError(
                        "chercher() attend exactement un argument",
                        node
                    )

                if not isinstance(arguments[0], str):
                    raise PyQRuntimeError(
                        "chercher() attend une chaîne",
                        node
                    )

                return target.find(arguments[0])

            if node.name == "compter":
                if len(arguments) != 1:
                    raise PyQRuntimeError(
                        "compter() attend exactement un argument",
                        node
                    )

                if not isinstance(arguments[0], str):
                    raise PyQRuntimeError(
                        "compter() attend une chaîne",
                        node
                    )

                return target.count(arguments[0])

            if node.name == "est_entier":
                if len(arguments) != 0:
                    raise PyQRuntimeError(
                        "est_entier() n'attend aucun argument",
                        node
                    )

                return target.isdigit()

            if node.name == "est_lettre":
                if len(arguments) != 0:
                    raise PyQRuntimeError(
                        "est_lettre() n'attend aucun argument",
                        node
                    )

                return target.isalpha()

            raise PyQRuntimeError(
                f"Méthode de chaîne inconnue : {node.name}",
                node
            )

        raise PyQRuntimeError(
            f"Méthode inconnue : {node.name}",
            node
        )

    def execute_FunctionCall(self, node):
        try:
            function = self.environment.get(node.name)

        except KeyError:
            raise PyQRuntimeError(
                f"Fonction inconnue : {node.name}",
                node
            )

        if not isinstance(function, Function):
            raise PyQRuntimeError(
                f"{node.name} n'est pas une fonction",
                node
            )

        if len(node.arguments) != len(function.parameters):
            raise PyQRuntimeError(
                f"La fonction {function.name} attend "
                f"{len(function.parameters)} argument(s), "
                f"mais {len(node.arguments)} ont été fournis",
                node
            )

        arguments = [
            self.execute(argument)
            for argument in node.arguments
        ]

        function_environment = Environment(
            function.closure
        )

        for parameter, argument in zip(
            function.parameters,
            arguments
        ):
            function_environment.define(
                parameter,
                argument
            )

        previous_environment = self.environment
        self.environment = function_environment

        try:
            for statement in function.body:
                self.execute(statement)

        except ReturnSignal as signal:
            return signal.value

        finally:
            self.environment = previous_environment

        return None

    def execute_VariableAssignment(self, node):
        value = self.execute(node.value)

        self.environment.set(
            node.name,
            value
        )

        return value

    def execute_IndexAssignment(self, node):
        target = self.execute(node.target)
        index = self.execute(node.index)
        value = self.execute(node.value)

        if isinstance(target, list):
            if not isinstance(index, int):
                raise PyQRuntimeError(
                    "L'index d'une liste doit être un entier",
                    node
                )

            if index < 0 or index >= len(target):
                raise PyQRuntimeError(
                    f"Index de liste hors limites : {index}",
                    node
                )

            target[index] = value
            return value

        if isinstance(target, dict):
            try:
                target[index] = value
            except TypeError:
                raise PyQRuntimeError(
                    "Clé de dictionnaire invalide",
                    node
                )

            return value

        if isinstance(target, str):
            raise PyQRuntimeError(
                "Une chaîne ne peut pas être modifiée",
                node
            )

        raise PyQRuntimeError(
            "Cet élément ne peut pas être modifié avec un index",
            node
        )

    def execute_FunctionDefinition(self, node):
        function = Function(
            node.name,
            node.parameters,
            node.body,
            self.environment
        )

        self.environment.define(
            node.name,
            function
        )

        return None

    def execute_ReturnStatement(self, node):
        value = None

        if node.value is not None:
            value = self.execute(node.value)

        raise ReturnSignal(value)

    def execute_BinaryOperation(self, node):
        left = self.execute(node.left)
        right = self.execute(node.right)

        if node.operator == "+":
            return left + right

        if node.operator == "-":
            return left - right

        if node.operator == "*":
            return left * right

        if node.operator == "/":
            return left / right

        raise PyQRuntimeError(
            f"Opérateur inconnu : {node.operator}",
            node
        )

    def execute_Comparison(self, node):
        left = self.execute(node.left)
        right = self.execute(node.right)

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

        raise PyQRuntimeError(
            f"Opérateur de comparaison inconnu : {node.operator}",
            node
        )

    def execute_LogicalOperation(self, node):
        if node.operator == "et":
            left = self.execute(node.left)

            if not self.is_truthy(left):
                return False

            return self.is_truthy(
                self.execute(node.right)
            )

        if node.operator == "ou":
            left = self.execute(node.left)

            if self.is_truthy(left):
                return True

            return self.is_truthy(
                self.execute(node.right)
            )

        raise PyQRuntimeError(
            f"Opérateur logique inconnu : {node.operator}",
            node
        )

    def execute_UnaryOperation(self, node):
        value = self.execute(node.operand)

        if node.operator == "non":
            return not self.is_truthy(value)

        if node.operator == "-":
            return -value

        raise PyQRuntimeError(
            f"Opérateur unaire inconnu : {node.operator}",
            node
        )

    def execute_IfStatement(self, node):
        condition = self.execute(node.condition)

        if self.is_truthy(condition):
            for statement in node.body:
                self.execute(statement)

        elif node.else_body is not None:
            for statement in node.else_body:
                self.execute(statement)

        return None

    def execute_WhileStatement(self, node):
        while self.is_truthy(
            self.execute(node.condition)
        ):
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
                "L'élément utilisé avec 'dans' n'est pas parcourable",
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
        if value is None:
            return False

        if value is False:
            return False

        if value == 0:
            return False

        if value == "":
            return False

        if isinstance(value, (list, dict)) and len(value) == 0:
            return False

        return True

    def print_value(self, value):
        if value is None:
            print("nul")
            return

        if value is True:
            print("vrai")
            return

        if value is False:
            print("faux")
            return

        if isinstance(value, list):
            print(
                "[" +
                ", ".join(
                    self.format_value(item)
                    for item in value
                ) +
                "]"
            )
            return

        if isinstance(value, dict):
            items = []

            for key, item in value.items():
                items.append(
                    f"{self.format_value(key)}: "
                    f"{self.format_value(item)}"
                )

            print(
                "{" +
                ", ".join(items) +
                "}"
            )
            return

        print(value)

    def format_value(self, value):
        if value is None:
            return "nul"

        if value is True:
            return "vrai"

        if value is False:
            return "faux"

        if isinstance(value, str):
            return value

        if isinstance(value, list):
            return (
                "[" +
                ", ".join(
                    self.format_value(item)
                    for item in value
                ) +
                "]"
            )

        if isinstance(value, dict):
            items = []

            for key, item in value.items():
                items.append(
                    f"{self.format_value(key)}: "
                    f"{self.format_value(item)}"
                )

            return (
                "{" +
                ", ".join(items) +
                "}"
            )

        return str(value)