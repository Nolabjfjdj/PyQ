from dataclasses import dataclass


class Node:
    pass


@dataclass
class Program(Node):
    statements: list


@dataclass
class StringLiteral(Node):
    value: str


@dataclass
class NumberLiteral(Node):
    value: int | float


@dataclass
class BooleanLiteral(Node):
    value: bool


@dataclass
class NullLiteral(Node):
    pass


@dataclass
class Identifier(Node):
    name: str


@dataclass
class ListLiteral(Node):
    elements: list


@dataclass
class ListAccess(Node):
    list_node: Node
    index: Node


@dataclass
class FunctionCall(Node):
    name: str
    arguments: list


@dataclass
class VariableAssignment(Node):
    name: str
    value: Node


@dataclass
class ListAssignment(Node):
    list_node: Node
    index: Node
    value: Node


@dataclass
class FunctionDefinition(Node):
    name: str
    parameters: list
    body: list


@dataclass
class ReturnStatement(Node):
    value: Node | None


@dataclass
class BinaryOperation(Node):
    left: Node
    operator: str
    right: Node


@dataclass
class Comparison(Node):
    left: Node
    operator: str
    right: Node


@dataclass
class LogicalOperation(Node):
    left: Node
    operator: str
    right: Node


@dataclass
class UnaryOperation(Node):
    operator: str
    operand: Node


@dataclass
class IfStatement(Node):
    condition: Node
    body: list
    else_body: list | None = None


@dataclass
class WhileStatement(Node):
    condition: Node
    body: list


@dataclass
class ForStatement(Node):
    variable: str
    iterable: Node
    body: list


@dataclass
class BreakStatement(Node):
    pass


@dataclass
class ContinueStatement(Node):
    pass