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
    ContinueStatement,
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
        method = getattr(
            self,
            f"execute_{type(node).__name__}",
            None
        )

        if method is None:
            raise PyQRuntimeError(
                f"Type de nœud non pris en charge : "
                f"{type(node).__name__}",
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
                if isinstance(index, int):
                    raise PyQRuntimeError(
                        f"Index de chaîne hors limites : {index}",
                        node
                    )

                raise PyQRuntimeError(
                    "Index de chaîne invalide",
                    node
                )

            if isinstance(target, list):
                if isinstance(index, int):
                    raise PyQRuntimeError(
                        f"Index de liste hors limites : {index}",
                        node
                    )

                raise PyQRuntimeError(
                    "Index de liste invalide",
                    node
                )

            if isinstance(target, dict):
                raise PyQRuntimeError(
                    f"Clé inexistante : {index}",
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
                        "Élément introuvable dans la liste",
                        node
                    )

                return None

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

            if node.name == "titre":
                if len(arguments) != 0:
                    raise PyQRuntimeError(
                        "titre() n'attend aucun argument",
                        node
                    )

                return target.title()

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

                return target.strip(arguments[0])

            if node.name == "chercher":
                if len(arguments) != 1:
                    raise PyQRuntimeError(
                        "chercher() attend exactement un argument",
                        node
                    )

                return target.find(arguments[0])

            if node.name == "compter":
                if len(arguments) != 1:
                    raise PyQRuntimeError(
                        "compter() attend exactement un argument",
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

            if node.name == "est_minuscule":
                if len(arguments) != 0:
                    raise PyQRuntimeError(
                        "est_minuscule() n'attend aucun argument",
                        node
                    )

                return target.islower()

            if node.name == "est_majuscule":
                if len(arguments) != 0:
                    raise PyQRuntimeError(
                        "est_majuscule() n'attend aucun argument",
                        node
                    )

                return target.isupper()

            if node.name == "est_alphanumerique":
                if len(arguments) != 0:
                    raise PyQRuntimeError(
                        "est_alphanumerique() n'attend aucun argument",
                        node
                    )

                return target.isalnum()

            if node.name == "est_espace":
                if len(arguments) != 0:
                    raise PyQRuntimeError(
                        "est_espace() n'attend aucun argument",
                        node
                    )

                return target.isspace()

            if node.name == "est_decimal":
                if len(arguments) != 0:
                    raise PyQRuntimeError(
                        "est_decimal() n'attend aucun argument",
                        node
                    )

                if target == "":
                    return False

                try:
                    float(target)
                    return "." in target

                except ValueError:
                    return False

            if node.name == "est_vide":
                if len(arguments) != 0:
                    raise PyQRuntimeError(
                        "est_vide() n'attend aucun argument",
                        node
                    )

                return target == ""

            if node.name == "debut":
                if len(arguments) != 1:
                    raise PyQRuntimeError(
                        "debut() attend exactement un argument",
                        node
                    )

                if not isinstance(arguments[0], int):
                    raise PyQRuntimeError(
                        "debut() attend un entier",
                        node
                    )

                return target[:arguments[0]]

            if node.name == "fin":
                if len(arguments) != 1:
                    raise PyQRuntimeError(
                        "fin() attend exactement un argument",
                        node
                    )

                if not isinstance(arguments[0], int):
                    raise PyQRuntimeError(
                        "fin() attend un entier",
                        node
                    )

                return (
                    target[-arguments[0]:]
                    if arguments[0] != 0
                    else ""
                )

        raise PyQRuntimeError(
            f"Méthode inconnue : {node.name}",
            node
        )

    def execute_FunctionCall(self, node):
        arguments = [
            self.execute(argument)
            for argument in node.arguments
        ]

        if node.name == "afficher":
            if len(arguments) != 1:
                raise PyQRuntimeError(
                    "afficher() attend exactement un argument",
                    node
                )

            self.print_value(arguments[0])
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
                f"{node.name} n'est pas une fonction",
                node
            )

        if len(arguments) != len(function.parameters):
            raise PyQRuntimeError(
                f"La fonction {function.name} attend "
                f"{len(function.parameters)} argument(s), "
                f"mais {len(arguments)} ont été fournis",
                node
            )

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

        try:
            target[index] = value

        except (IndexError, KeyError, TypeError):
            if isinstance(target, list):
                raise PyQRuntimeError(
                    f"Index de liste invalide : {index}",
                    node
                )

            if isinstance(target, dict):
                raise PyQRuntimeError(
                    f"Impossible de modifier la clé : {index}",
                    node
                )

            raise PyQRuntimeError(
                "Modification par index impossible",
                node
            )

        return value

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
            f"Opérateur de comparaison inconnu : "
            f"{node.operator}",
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

        if node.operator == "-":
            try:
                return -operand

            except TypeError:
                raise PyQRuntimeError(
                    "Impossible de changer le signe de cette valeur",
                    node
                )

        raise PyQRuntimeError(
            f"Opérateur unaire inconnu : {node.operator}",
            node
        )

    def execute_IfStatement(self, node):
        if self.is_truthy(
            self.execute(node.condition)
        ):
            for statement in node.body:
                self.execute(statement)

            return None

        if node.else_body is not None:
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
            values = iter(iterable)

        except TypeError:
            raise PyQRuntimeError(
                "La valeur utilisée avec 'dans' n'est pas parcourable",
                node
            )

        for value in values:
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
                "["
                + ", ".join(
                    self.format_value(item)
                    for item in value
                )
                + "]"
            )
            return

        if isinstance(value, dict):
            entries = []

            for key, item in value.items():
                entries.append(
                    f"{self.format_value(key)}: "
                    f"{self.format_value(item)}"
                )

            print(
                "{"
                + ", ".join(entries)
                + "}"
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
                "["
                + ", ".join(
                    self.format_value(item)
                    for item in value
                )
                + "]"
            )

        if isinstance(value, dict):
            entries = []

            for key, item in value.items():
                entries.append(
                    f"{self.format_value(key)}: "
                    f"{self.format_value(item)}"
                )

            return (
                "{"
                + ", ".join(entries)
                + "}"
            )

        return str(value)