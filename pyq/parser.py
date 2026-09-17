from .ast import Program, StringLiteral, FunctionCall


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
            statements.append(self.parse_function_call())

        return Program(statements)

    def parse_function_call(self):
        name = self.expect("IDENTIFIER").value

        self.expect("LPAREN")

        argument_token = self.expect("STRING")

        argument = StringLiteral(argument_token.value)

        self.expect("RPAREN")

        return FunctionCall(name, argument)