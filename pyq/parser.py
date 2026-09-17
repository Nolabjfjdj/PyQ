from .ast import (
    Program,
    StringLiteral,
    NumberLiteral,
    BooleanLiteral,
    Identifier,
    FunctionCall,
    VariableAssignment,
    BinaryOperation,
    Comparison,
    LogicalOperation,
    UnaryOperation,
    IfStatement,
    WhileStatement,
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

    def skip_newlines(self):
        while self.current().type == "NEWLINE":
            self.advance()

    def parse(self):
        statements = []

        self.skip_newlines()

        while self.current().type != "EOF":
            if self.current().type == "DEDENT":
                self.advance()
                continue

            statements.append(self.parse_statement())

            self.skip_newlines()

        return Program(statements)

    def parse_statement(self):
        token = self.current()

        if token.type != "IDENTIFIER":
            raise SyntaxError(
                f"Instruction invalide à la position {token.position}"
            )

        if token.value == "si":
            return self.parse_if()

        if token.value == "tantque":
            return self.parse_while()

        if token.value == "sinon":
            raise SyntaxError(
                f"'sinon' inattendu à la position {token.position}"
            )

        next_token = self.tokens[self.position + 1]

        if next_token.type == "EQUALS":
            statement = self.parse_assignment()
        else:
            statement = self.parse_function_call()

        if self.current().type == "NEWLINE":
            self.advance()

        return statement

    def parse_if(self):
        self.expect("IDENTIFIER")

        condition = self.parse_expression()

        self.expect("COLON")
        self.expect("NEWLINE")
        self.expect("INDENT")

        body = []

        self.skip_newlines()

        while self.current().type not in ("DEDENT", "EOF"):
            body.append(self.parse_statement())
            self.skip_newlines()

        if self.current().type == "DEDENT":
            self.advance()

        else_body = None

        if (
            self.current().type == "IDENTIFIER"
            and self.current().value == "sinon"
        ):
            self.advance()

            self.expect("COLON")
            self.expect("NEWLINE")
            self.expect("INDENT")

            else_body = []

            self.skip_newlines()

            while self.current().type not in ("DEDENT", "EOF"):
                else_body.append(self.parse_statement())
                self.skip_newlines()

            if self.current().type == "DEDENT":
                self.advance()

        return IfStatement(
            condition,
            body,
            else_body
        )

    def parse_while(self):
        self.expect("IDENTIFIER")

        condition = self.parse_expression()

        self.expect("COLON")
        self.expect("NEWLINE")
        self.expect("INDENT")

        body = []

        self.skip_newlines()

        while self.current().type not in ("DEDENT", "EOF"):
            body.append(self.parse_statement())
            self.skip_newlines()

        if self.current().type == "DEDENT":
            self.advance()

        return WhileStatement(
            condition,
            body
        )

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
        return self.parse_or()

    def parse_or(self):
        expression = self.parse_and()

        while (
            self.current().type == "IDENTIFIER"
            and self.current().value == "ou"
        ):
            self.advance()

            right = self.parse_and()

            expression = LogicalOperation(
                expression,
                "ou",
                right
            )

        return expression

    def parse_and(self):
        expression = self.parse_comparison()

        while (
            self.current().type == "IDENTIFIER"
            and self.current().value == "et"
        ):
            self.advance()

            right = self.parse_comparison()

            expression = LogicalOperation(
                expression,
                "et",
                right
            )

        return expression

    def parse_comparison(self):
        expression = self.parse_unary()

        comparison_operators = {
            "EQUALS_EQUALS",
            "NOT_EQUALS",
            "GREATER",
            "LESS",
            "GREATER_EQUALS",
            "LESS_EQUALS",
        }

        while self.current().type in comparison_operators:
            operator = self.advance().value
            right = self.parse_unary()

            expression = Comparison(
                expression,
                operator,
                right
            )

        return expression

    def parse_unary(self):
        if (
            self.current().type == "IDENTIFIER"
            and self.current().value == "non"
        ):
            self.advance()

            operand = self.parse_unary()

            return UnaryOperation(
                "non",
                operand
            )

        return self.parse_addition()

    def parse_addition(self):
        expression = self.parse_multiplication()

        while self.current().type in ("PLUS", "MINUS"):
            operator = self.advance().value
            right = self.parse_multiplication()

            expression = BinaryOperation(
                expression,
                operator,
                right
            )

        return expression

    def parse_multiplication(self):
        expression = self.parse_primary()

        while self.current().type in ("STAR", "SLASH"):
            operator = self.advance().value
            right = self.parse_primary()

            expression = BinaryOperation(
                expression,
                operator,
                right
            )

        return expression

    def parse_primary(self):
        token = self.current()

        if token.type == "STRING":
            self.advance()
            return StringLiteral(token.value)

        if token.type == "NUMBER":
            self.advance()
            return NumberLiteral(int(token.value))

        if token.type == "IDENTIFIER":
            self.advance()

            if token.value == "vrai":
                return BooleanLiteral(True)

            if token.value == "faux":
                return BooleanLiteral(False)

            return Identifier(token.value)

        if token.type == "LPAREN":
            self.advance()

            expression = self.parse_expression()

            self.expect("RPAREN")

            return expression

        raise SyntaxError(
            f"Expression invalide à la position {token.position}"
        )