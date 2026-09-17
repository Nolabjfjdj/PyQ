from .ast import (
    Program,
    StringLiteral,
    NumberLiteral,
    Identifier,
    FunctionCall,
    VariableAssignment,
)


class Parser:
    def __init__(self, tokens):
        self.tokens = tokens
        self.position = 0

    def current(self):
        return self.tokens[self.position]

    def advance(self):
        token = self.current()
        self.position += 1
        return token

    def expect(self, token_type):
        token = self.current()

        if token.type != token_type:
            raise SyntaxError(
                f"Attendu {token_type}, obtenu {token.type}"
            )

        return self.advance()

    def parse(self):
        statements = []

        while self.current().type != "EOF":
            statements.append(self.parse_statement())

        return Program(statements)

    def parse_statement(self):
        token = self.current()

        if token.type != "IDENTIFIER":
            raise SyntaxError(
                f"Instruction invalide à la position {token.position}"
            )

        next_token = self.tokens[self.position + 1]

        if next_token.type == "EQUALS":
            return self.parse_assignment()

        return self.parse_function_call()

    def parse_assignment(self):
        name = self.expect("IDENTIFIER").value

        self.expect("EQUALS")

        value = self.parse_expression()

        return VariableAssignment(name, value)

    def parse_function_call(self):
        name = self.expect("IDENTIFIER").value

        self.expect("LPAREN")

        argument = self.parse_expression()

        self.expect("RPAREN")

        return FunctionCall(name, argument)

    def parse_expression(self):
        token = self.current()

        if token.type == "STRING":
            self.advance()
            return StringLiteral(token.value)

        if token.type == "NUMBER":
            self.advance()
            return NumberLiteral(int(token.value))

        if token.type == "IDENTIFIER":
            self.advance()
            return Identifier(token.value)

        raise SyntaxError(
            f"Expression invalide à la position {token.position}"
        )