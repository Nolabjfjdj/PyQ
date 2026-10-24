import math
from pathlib import Path

from pyq.lexer import Lexer
from pyq.parser import Parser

from pyq.ast import (
    Program,
    StringLiteral,
    NumberLiteral,
    BooleanLiteral,
    NullLiteral,
    Identifier,
    ListLiteral,
    TupleLiteral,
    ListComprehension,
    DictLiteral,
    DictComprehension,
    IndexAccess,
    SliceAccess,
    MethodCall,
    FunctionCall,
    NamedArgument,
    ImportStatement,
    VariableAssignment,
    CompoundAssignment,
    IndexAssignment,
    FunctionDefinition,
    ReturnStatement,
    RaiseStatement,
    BinaryOperation,
    Comparison,
    LogicalOperation,
    UnaryOperation,
    IfStatement,
    WhileStatement,
    ForStatement,
    BreakStatement,
    ContinueStatement,
    TryStatement,
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
    def __init__(self, name, parameters, body, closure, defaults):
        self.name = name
        self.parameters = parameters
        self.body = body
        self.closure = closure
        self.defaults = defaults


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
    def __init__(self, base_dir=None):
        self.environment = Environment()
        self.base_dir = Path(base_dir) if base_dir is not None else Path.cwd()
        self.imported_files = set()

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

    def execute_TupleLiteral(self, node):
        return tuple(
            self.execute(element)
            for element in node.elements
        )

    def execute_ListComprehension(self, node):
        iterable = self.execute(node.iterable)

        try:
            values = iter(iterable)
        except TypeError:
            raise PyQRuntimeError(
                "La valeur utilisée dans une compréhension de liste n'est pas parcourable",
                node
            )

        result = []
        previous_environment = self.environment
        comprehension_environment = Environment(previous_environment)
        self.environment = comprehension_environment

        try:
            for value in values:
                comprehension_environment.define(node.variable, value)

                if (
                    node.condition is not None
                    and not self.is_truthy(self.execute(node.condition))
                ):
                    continue

                result.append(self.execute(node.element))
        finally:
            self.environment = previous_environment

        return result

    def execute_DictLiteral(self, node):
        result = {}

        for key_node, value_node in node.entries:
            key = self.execute(key_node)
            value = self.execute(value_node)
            result[key] = value

        return result

    def execute_DictComprehension(self, node):
        iterable = self.execute(node.iterable)

        try:
            values = iter(iterable)
        except TypeError:
            raise PyQRuntimeError(
                "La valeur utilisée dans une compréhension de dictionnaire n'est pas parcourable",
                node
            )

        result = {}
        previous_environment = self.environment
        comprehension_environment = Environment(previous_environment)
        self.environment = comprehension_environment

        try:
            for item in values:
                comprehension_environment.define(node.variable, item)

                if (
                    node.condition is not None
                    and not self.is_truthy(self.execute(node.condition))
                ):
                    continue

                key = self.execute(node.key)
                value = self.execute(node.value)

                try:
                    result[key] = value
                except TypeError:
                    raise PyQRuntimeError(
                        "La clé créée dans la compréhension de dictionnaire n'est pas valide",
                        node
                    )
        finally:
            self.environment = previous_environment

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

            if isinstance(target, tuple):
                if isinstance(index, int):
                    raise PyQRuntimeError(
                        f"Index de tuple hors limites : {index}",
                        node
                    )

                raise PyQRuntimeError(
                    "Index de tuple invalide",
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

    def execute_SliceAccess(self, node):
        target = self.execute(node.target)

        start = (
            self.execute(node.start)
            if node.start is not None
            else None
        )

        end = (
            self.execute(node.end)
            if node.end is not None
            else None
        )

        step = (
            self.execute(node.step)
            if node.step is not None
            else None
        )

        for name, value in (
            ("début", start),
            ("fin", end),
            ("pas", step),
        ):
            if value is not None and not isinstance(value, int):
                raise PyQRuntimeError(
                    f"L'indice de {name} doit être un entier",
                    node
                )

        if step == 0:
            raise PyQRuntimeError(
                "Le pas d'une tranche ne peut pas être zéro",
                node
            )

        if not isinstance(target, (str, list, tuple)):
            raise PyQRuntimeError(
                "La découpe est disponible uniquement pour les chaînes, les listes et les tuples",
                node
            )

        try:
            return target[slice(start, end, step)]

        except (TypeError, ValueError):
            raise PyQRuntimeError(
                "Découpe impossible avec ces indices",
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

            if node.name == "inverser":
                if len(arguments) != 0:
                    raise PyQRuntimeError(
                        "inverser() n'attend aucun argument",
                        node
                    )

                return target[::-1]

            if node.name == "repetitions":
                if len(arguments) != 1:
                    raise PyQRuntimeError(
                        "repetitions() attend exactement un argument",
                        node
                    )

                if not isinstance(arguments[0], int):
                    raise PyQRuntimeError(
                        "repetitions() attend un entier",
                        node
                    )

                if arguments[0] < 0:
                    raise PyQRuntimeError(
                        "repetitions() attend un entier positif ou nul",
                        node
                    )

                return target * arguments[0]

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

            if node.name == "position":
                if len(arguments) != 1:
                    raise PyQRuntimeError(
                        "position() attend exactement un argument",
                        node
                    )

                position = target.find(arguments[0])

                if position == -1:
                    raise PyQRuntimeError(
                        f"Texte introuvable : {arguments[0]}",
                        node
                    )

                return position

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

            if node.name == "retirer_debut":
                if len(arguments) != 1:
                    raise PyQRuntimeError(
                        "retirer_debut() attend exactement un argument",
                        node
                    )

                if not isinstance(arguments[0], int):
                    raise PyQRuntimeError(
                        "retirer_debut() attend un entier",
                        node
                    )

                if arguments[0] < 0:
                    raise PyQRuntimeError(
                        "retirer_debut() attend un entier positif ou nul",
                        node
                    )

                return target[arguments[0]:]

        raise PyQRuntimeError(
            f"Méthode inconnue : {node.name}",
            node
        )

    def execute_ImportStatement(self, node):
        path_value = self.execute(node.path)

        if not isinstance(path_value, str):
            raise PyQRuntimeError(
                "importer() attend le chemin du module sous forme de chaîne de caractères",
                node
            )

        module_path = Path(path_value)

        if not module_path.is_absolute():
            module_path = self.base_dir / module_path

        if module_path.suffix == "":
            module_path = module_path.with_suffix(".pyq")

        module_path = module_path.resolve()

        if not module_path.exists():
            raise PyQRuntimeError(
                f"Module introuvable : {path_value}",
                node
            )

        if module_path in self.imported_files:
            return None

        try:
            source = module_path.read_text(encoding="utf-8")
        except OSError as error:
            raise PyQRuntimeError(
                f"Impossible de lire le module : {error}",
                node
            )

        self.imported_files.add(module_path)

        lexer = Lexer(source)
        tokens = lexer.tokenize()
        parser = Parser(tokens)
        program = parser.parse()

        previous_base_dir = self.base_dir
        self.base_dir = module_path.parent

        try:
            self.execute(program)
        except PyQRuntimeError:
            raise
        finally:
            self.base_dir = previous_base_dir

        return None

    def execute_FunctionCall(self, node):
        positional_arguments = []
        named_arguments = {}
        named_started = False

        for argument in node.arguments:
            if isinstance(argument, NamedArgument):
                named_started = True

                if argument.name in named_arguments:
                    raise PyQRuntimeError(
                        f"Argument nommé fourni plusieurs fois : {argument.name}",
                        node
                    )

                named_arguments[argument.name] = self.execute(argument.value)
            else:
                if named_started:
                    raise PyQRuntimeError(
                        "Un argument positionnel ne peut pas suivre un argument nommé",
                        node
                    )

                positional_arguments.append(self.execute(argument))

        arguments = positional_arguments

        if node.name == "puissance":
            if len(arguments) != 2 or named_arguments:
                raise PyQRuntimeError(
                    "puissance() attend exactement deux arguments : la base et l'exposant",
                    node
                )

            base, exponent = arguments

            if (
                not isinstance(base, (int, float))
                or isinstance(base, bool)
                or not isinstance(exponent, (int, float))
                or isinstance(exponent, bool)
            ):
                raise PyQRuntimeError(
                    "puissance() attend deux nombres",
                    node
                )

            try:
                return base ** exponent
            except (OverflowError, ZeroDivisionError, ValueError) as error:
                raise PyQRuntimeError(
                    "Impossible de calculer cette puissance",
                    node
                ) from error

        if node.name == "factorielle":
            if len(arguments) != 1 or named_arguments:
                raise PyQRuntimeError(
                    "factorielle() attend exactement un argument",
                    node
                )

            value = arguments[0]

            if not isinstance(value, int) or isinstance(value, bool):
                raise PyQRuntimeError(
                    "factorielle() attend un entier",
                    node
                )

            if value < 0:
                raise PyQRuntimeError(
                    "factorielle() attend un entier positif ou nul",
                    node
                )

            return math.factorial(value)

        if node.name == "racine_carree":
            if len(arguments) != 1 or named_arguments:
                raise PyQRuntimeError(
                    "racine_carree() attend exactement un argument",
                    node
                )

            value = arguments[0]

            if not isinstance(value, (int, float)) or isinstance(value, bool):
                raise PyQRuntimeError(
                    "racine_carree() attend un nombre",
                    node
                )

            if value < 0:
                raise PyQRuntimeError(
                    "racine_carree() ne peut pas calculer la racine d'un nombre négatif",
                    node
                )

            return math.sqrt(value)

        if node.name == "arrondir":
            if named_arguments or len(arguments) not in (1, 2):
                raise PyQRuntimeError(
                    "arrondir() attend un nombre et éventuellement le nombre de décimales",
                    node
                )

            value = arguments[0]
            digits = arguments[1] if len(arguments) == 2 else 0

            if not isinstance(value, (int, float)) or isinstance(value, bool):
                raise PyQRuntimeError(
                    "arrondir() attend un nombre à arrondir",
                    node
                )

            if not isinstance(digits, int) or isinstance(digits, bool):
                raise PyQRuntimeError(
                    "Le nombre de décimales d'arrondir() doit être un entier",
                    node
                )

            return round(value, digits)

        if node.name == "valeur_absolue":
            if len(arguments) != 1 or named_arguments:
                raise PyQRuntimeError(
                    "valeur_absolue() attend exactement un argument",
                    node
                )

            value = arguments[0]

            if not isinstance(value, (int, float)) or isinstance(value, bool):
                raise PyQRuntimeError(
                    "valeur_absolue() attend un nombre",
                    node
                )

            return abs(value)

        if node.name == "somme":
            if named_arguments or len(arguments) not in (1, 2):
                raise PyQRuntimeError(
                    "somme() attend un itérable et éventuellement une valeur de départ",
                    node
                )

            iterable = arguments[0]
            start = arguments[1] if len(arguments) == 2 else 0

            if not isinstance(iterable, (list, tuple, range)):
                raise PyQRuntimeError(
                    "somme() attend une liste, un tuple ou un intervalle",
                    node
                )

            if not isinstance(start, (int, float)) or isinstance(start, bool):
                raise PyQRuntimeError(
                    "La valeur de départ de somme() doit être un nombre",
                    node
                )

            total = start

            for value in iterable:
                if not isinstance(value, (int, float)) or isinstance(value, bool):
                    raise PyQRuntimeError(
                        "somme() ne peut additionner que des nombres",
                        node
                    )

                total += value

            return total

        if node.name in ("minimum", "maximum"):
            if named_arguments:
                raise PyQRuntimeError(
                    f"{node.name}() n'accepte pas d'arguments nommés",
                    node
                )

            if len(arguments) == 0:
                raise PyQRuntimeError(
                    f"{node.name}() attend au moins un argument",
                    node
                )

            if len(arguments) == 1:
                iterable = arguments[0]

                if not isinstance(iterable, (str, list, tuple, range, dict)):
                    raise PyQRuntimeError(
                        f"{node.name}() attend une chaîne, une liste, un tuple, un dictionnaire ou un intervalle",
                        node
                    )

                values = list(iterable)

                if not values:
                    raise PyQRuntimeError(
                        f"{node.name}() ne peut pas être utilisé avec une collection vide",
                        node
                    )
            else:
                values = arguments

            try:
                result = values[0]

                for value in values[1:]:
                    if (
                        (node.name == "minimum" and value < result)
                        or (node.name == "maximum" and value > result)
                    ):
                        result = value

                return result
            except TypeError:
                raise PyQRuntimeError(
                    f"{node.name}() ne peut pas comparer ces valeurs entre elles",
                    node
                )

        if node.name == "taille":
            if len(arguments) != 1 or named_arguments:
                raise PyQRuntimeError(
                    "taille() attend exactement un argument",
                    node
                )

            value = arguments[0]

            if isinstance(value, (str, list, tuple, dict, range)):
                return len(value)

            raise PyQRuntimeError(
                "taille() attend une chaîne, une liste, un tuple, un dictionnaire ou un intervalle",
                node
            )

        if node.name == "intervalle":
            if named_arguments:
                raise PyQRuntimeError(
                    "intervalle() n'accepte pas d'arguments nommés",
                    node
                )

            if len(arguments) not in (1, 2, 3):
                raise PyQRuntimeError(
                    "intervalle() attend un, deux ou trois arguments",
                    node
                )

            if not all(
                isinstance(value, int) and not isinstance(value, bool)
                for value in arguments
            ):
                raise PyQRuntimeError(
                    "Les arguments d'intervalle() doivent être des entiers",
                    node
                )

            if len(arguments) == 1:
                return range(arguments[0])

            if len(arguments) == 2:
                return range(arguments[0], arguments[1])

            if arguments[2] == 0:
                raise PyQRuntimeError(
                    "Le pas d'intervalle() ne peut pas être zéro",
                    node
                )

            return range(
                arguments[0],
                arguments[1],
                arguments[2]
            )

        if node.name == "afficher":
            if len(arguments) != 1 or named_arguments:
                raise PyQRuntimeError(
                    "afficher() attend exactement un argument",
                    node
                )

            self.print_value(arguments[0])
            return None

        if node.name == "demander":
            if len(arguments) != 1 or named_arguments:
                raise PyQRuntimeError(
                    "demander() attend exactement un argument",
                    node
                )

            if not isinstance(arguments[0], str):
                raise PyQRuntimeError(
                    "demander() attend une chaîne de caractères",
                    node
                )

            try:
                return input(arguments[0])
            except EOFError:
                return ""

        if node.name == "lire_fichier":
            if len(arguments) != 1 or named_arguments:
                raise PyQRuntimeError(
                    "lire_fichier() attend exactement un argument",
                    node
                )

            if not isinstance(arguments[0], str):
                raise PyQRuntimeError(
                    "lire_fichier() attend un chemin sous forme de chaîne de caractères",
                    node
                )

            path = self.base_dir / arguments[0]

            try:
                return path.read_text(encoding="utf-8")
            except OSError as error:
                raise PyQRuntimeError(
                    f"Impossible de lire le fichier : {arguments[0]}",
                    node
                ) from error

        if node.name == "écrire_fichier":
            if len(arguments) != 2 or named_arguments:
                raise PyQRuntimeError(
                    "écrire_fichier() attend exactement deux arguments",
                    node
                )

            if not isinstance(arguments[0], str):
                raise PyQRuntimeError(
                    "écrire_fichier() attend un chemin sous forme de chaîne de caractères",
                    node
                )

            if not isinstance(arguments[1], str):
                raise PyQRuntimeError(
                    "écrire_fichier() attend un contenu sous forme de chaîne de caractères",
                    node
                )

            path = self.base_dir / arguments[0]

            try:
                path.parent.mkdir(parents=True, exist_ok=True)
                path.write_text(arguments[1], encoding="utf-8")
            except OSError as error:
                raise PyQRuntimeError(
                    f"Impossible d'écrire le fichier : {arguments[0]}",
                    node
                ) from error

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

        if len(positional_arguments) > len(function.parameters):
            raise PyQRuntimeError(
                f"La fonction {function.name} attend au maximum {len(function.parameters)} argument(s), "
                f"mais {len(positional_arguments)} ont été fournis",
                node
            )

        parameter_values = {}

        for index, value in enumerate(positional_arguments):
            parameter_values[function.parameters[index]] = value

        parameter_names = set(function.parameters)

        for name, value in named_arguments.items():
            if name not in parameter_names:
                raise PyQRuntimeError(
                    f"La fonction {function.name} n'a pas de paramètre nommé : {name}",
                    node
                )

            if name in parameter_values:
                raise PyQRuntimeError(
                    f"L'argument {name} a été fourni plusieurs fois",
                    node
                )

            parameter_values[name] = value

        required_count = len(function.parameters) - len(function.defaults)

        missing_required = [
            parameter
            for parameter in function.parameters[:required_count]
            if parameter not in parameter_values
        ]

        if missing_required:
            raise PyQRuntimeError(
                f"La fonction {function.name} a des paramètres obligatoires manquants : "
                f"{', '.join(missing_required)}",
                node
            )

        function_environment = Environment(
            function.closure
        )

        default_start = required_count

        for index, parameter in enumerate(function.parameters):
            if parameter in parameter_values:
                value = parameter_values[parameter]
            else:
                value = function.defaults[index - default_start]

            function_environment.define(
                parameter,
                value
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

    def execute_CompoundAssignment(self, node):
        current = self.environment.get(node.name)
        value = self.execute(node.value)

        try:
            if node.operator == "+":
                result = current + value
            elif node.operator == "-":
                result = current - value
            elif node.operator == "*":
                result = current * value
            elif node.operator == "/":
                result = current / value
            elif node.operator == "//":
                result = current // value
            elif node.operator == "%":
                result = current % value
            elif node.operator == "**":
                result = current ** value
            else:
                raise PyQRuntimeError(
                    f"Opérateur d'affectation inconnu : {node.operator}",
                    node
                )

        except ZeroDivisionError:
            raise PyQRuntimeError(
                "Division par zéro",
                node
            )

        except TypeError:
            raise PyQRuntimeError(
                "Opération impossible entre ces valeurs",
                node
            )

        self.environment.set(
            node.name,
            result
        )

        return result

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
        parameters = []
        defaults = []

        for parameter, default_node in node.parameters:
            parameters.append(parameter)

            if default_node is not None:
                defaults.append(self.execute(default_node))

        function = Function(
            node.name,
            parameters,
            node.body,
            self.environment,
            defaults
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

    def execute_RaiseStatement(self, node):
        value = self.execute(node.value)

        if not isinstance(value, str):
            value = self.format_value(value)

        raise PyQRuntimeError(
            value,
            node
        )

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

            if node.operator == "//":
                return left // right

            if node.operator == "%":
                return left % right

            if node.operator == "**":
                return left ** right

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

            if node.operator == "est":
                return left is right

            if node.operator == "n'est pas":
                return left is not right

            if node.operator == "dans":
                return left in right

            if node.operator == "pas dans":
                return left not in right

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

        if node.operator in ("-", "+"):
            try:
                return (
                    -operand
                    if node.operator == "-"
                    else +operand
                )

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

    def execute_TryStatement(self, node):
        try:
            for statement in node.body:
                self.execute(statement)

        except PyQRuntimeError as error:
            if node.except_body is None:
                raise

            if node.except_name is not None:
                self.environment.set(
                    node.except_name,
                    error.message
                )

            for statement in node.except_body:
                self.execute(statement)

        finally:
            if node.finally_body is not None:
                for statement in node.finally_body:
                    self.execute(statement)

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

        if isinstance(value, tuple):
            contents = ", ".join(
                self.format_value(item)
                for item in value
            )
            if len(value) == 1:
                contents += ","
            print("(" + contents + ")")
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

        print(self.format_value(value))

    def format_value(self, value):
        if value is None:
            return "nul"

        if value is True:
            return "vrai"

        if value is False:
            return "faux"

        if isinstance(value, str):
            return value

        if isinstance(value, float) and value.is_integer():
            return str(int(value))

        if isinstance(value, list):
            return (
                "["
                + ", ".join(
                    self.format_value(item)
                    for item in value
                )
                + "]"
            )

        if isinstance(value, tuple):
            contents = ", ".join(
                self.format_value(item)
                for item in value
            )
            if len(value) == 1:
                contents += ","
            return "(" + contents + ")"

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