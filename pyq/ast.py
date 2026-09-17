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
class FunctionCall(Node):
    name: str
    argument: Node