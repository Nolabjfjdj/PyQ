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
class Identifier(Node):
    name: str


@dataclass
class NumberLiteral(Node):
    value: int


@dataclass
class FunctionCall(Node):
    name: str
    argument: Node


@dataclass
class VariableAssignment(Node):
    name: str
    value: Node