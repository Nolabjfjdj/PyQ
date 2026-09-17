from dataclasses import dataclass


class Node:
    pass


@dataclass
class Program(Node):
    statements: list
    line: int | None = None


@dataclass
class StringLiteral(Node):
    value: str
    line: int | None = None


@dataclass
class NumberLiteral(Node):
    value: int | float
    line: int | None = None


@dataclass
class BooleanLiteral(Node):
    value: bool
    line: int | None = None


@dataclass
class NullLiteral(Node):
    line: int | None = None


@dataclass
class Identifier(Node):
    name: str
    line: int | None = None


@dataclass
class ListLiteral(Node):
    elements: list
    line: int | None = None


@dataclass
class DictLiteral(Node):
    entries: list
    line: int | None = None


@dataclass
class IndexAccess(Node):
    target: Node
    index: Node
    line: int | None = None


@dataclass
class MethodCall(Node):
    target: Node
    name: str
    arguments: list
    line: int | None = None


@dataclass
class FunctionCall(Node):
    name: str
    arguments: list
    line: int | None = None


@dataclass
class VariableAssignment(Node):
    name: str
    value: Node
    line: int | None = None


@dataclass
class IndexAssignment(Node):
    target: Node
    index: Node
    value: Node
    line: int | None = None


@dataclass
class FunctionDefinition(Node):
    name: str
    parameters: list
    body: list
    line: int | None = None


@dataclass
class ReturnStatement(Node):
    value: Node | None
    line: int | None = None


@dataclass
class BinaryOperation(Node):
    left: Node
    operator: str
    right: Node
    line: int | None = None


@dataclass
class Comparison(Node):
    left: Node
    operator: str
    right: Node
    line: int | None = None


@dataclass
class LogicalOperation(Node):
    left: Node
    operator: str
    right: Node
    line: int | None = None


@dataclass
class UnaryOperation(Node):
    operator: str
    operand: Node
    line: int | None = None


@dataclass
class IfStatement(Node):
    condition: Node
    body: list
    else_body: list | None = None
    line: int | None = None


@dataclass
class WhileStatement(Node):
    condition: Node
    body: list
    line: int | None = None


@dataclass
class ForStatement(Node):
    variable: str
    iterable: Node
    body: list
    line: int | None = None


@dataclass
class BreakStatement(Node):
    line: int | None = None


@dataclass
class ContinueStatement(Node):
    line: int | None = None