from .ast import (
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

    def error(self, message, token=None):
        if token is None:
            token = self.current()

        raise SyntaxError(
            f"Erreur de syntaxe à la ligne {token.position} : {message}"
        )

    def expect(self, token_type):
        token = self.current()

        if token.type != token_type:
            self.error(
                f"attendu {token_type}, obtenu {token.type}",
                token
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
            self.error("instruction invalide", token)

        if token.value == "si":
            return self.parse_if()

        if token.value == "tantque":
            return self.parse_while()

        if token.value == "pour":
            return self.parse_for()

        if token.value == "fonction":
            return self.parse_function_definition()

        if token.value == "retourner":
            return self.parse_return()

        if token.value == "interrompre":
            self.advance()

            if self.current().type == "NEWLINE":
                self.advance()

            return BreakStatement()

        if token.value == "continuer":
            self.advance()

            if self.current().type == "NEWLINE":
                self.advance()

            return ContinueStatement()

        if token.value == "sinon":
            self.error(
                "'sinon' inattendu",
                token
            )

        next_token = self.tokens[self.position + 1]

        if next_token.type == "EQUALS":
            statement = self.parse_assignment()

        elif next_token.type == "LBRACKET":
            statement = self.parse_index_assignment()

        elif next_token.type == "DOT":
            statement = self.parse_expression()

        else:
            statement = self.parse_function_call()

        if self.current().type == "NEWLINE":
            self.advance()

        return statement

    def parse_function_definition(self):
        self.expect("IDENTIFIER")

        name = self.expect("IDENTIFIER").value

        self.expect("LPAREN")

        parameters = []

        if self.current().type != "RPAREN":
            while True:
                parameter = self.expect("IDENTIFIER").value
                parameters.append(parameter)

                if self.current().type != "COMMA":
                    break

                self.advance()

        self.expect("RPAREN")
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

        return FunctionDefinition(
            name,
            parameters,
            body
        )

    def parse_return(self):
        self.expect("IDENTIFIER")

        if self.current().type in ("NEWLINE", "DEDENT", "EOF"):
            return ReturnStatement(None)

        value = self.parse_expression()

        if self.current().type == "NEWLINE":
            self.advance()

        return ReturnStatement(value)

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

            if (
                self.current().type == "IDENTIFIER"
                and self.current().value == "si"
            ):
                else_body = [
                    self.parse_if()
                ]

                return IfStatement(
                    condition,
                    body,
                    else_body
                )

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

    def parse_for(self):
        self.expect("IDENTIFIER")

        variable = self.expect("IDENTIFIER").value

        if (
            self.current().type != "IDENTIFIER"
            or self.current().value != "dans"
        ):
            self.error(
                f"attendu 'dans', obtenu {self.current().value}"
            )

        self.advance()

        iterable = self.parse_expression()

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

        return ForStatement(
            variable,
            iterable,
            body
        )

    def parse_assignment(self):
        name = self.expect("IDENTIFIER").value

        self.expect("EQUALS")

        value = self.parse_expression()

        return VariableAssignment(name, value)

    def parse_index_assignment(self):
        name = self.expect("IDENTIFIER").value

        target = Identifier(name)

        self.expect("LBRACKET")

        index = self.parse_expression()

        self.expect("RBRACKET")
        self.expect("EQUALS")

        value = self.parse_expression()

        return IndexAssignment(
            target,
            index,
            value
        )

    def parse_function_call(self):
        name = self.expect("IDENTIFIER").value

        self.expect("LPAREN")

        arguments = []

        if self.current().type != "RPAREN":
            while True:
                arguments.append(self.parse_expression())

                if self.current().type != "COMMA":
                    break

                self.advance()

        self.expect("RPAREN")

        return FunctionCall(
            name,
            arguments
        )

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
            expression = StringLiteral(token.value)
            return self.parse_postfix(expression)

        if token.type == "NUMBER":
            self.advance()

            if "." in token.value:
                value = float(token.value)
            else:
                value = int(token.value)

            expression = NumberLiteral(value)
            return self.parse_postfix(expression)

        if token.type == "IDENTIFIER":
            self.advance()

            if token.value == "vrai":
                expression = BooleanLiteral(True)

            elif token.value == "faux":
                expression = BooleanLiteral(False)

            elif token.value == "nul":
                expression = NullLiteral()

            elif self.current().type == "LPAREN":
                self.advance()

                arguments = []

                if self.current().type != "RPAREN":
                    while True:
                        arguments.append(self.parse_expression())

                        if self.current().type != "COMMA":
                            break

                        self.advance()

                self.expect("RPAREN")

                expression = FunctionCall(
                    token.value,
                    arguments
                )

            else:
                expression = Identifier(token.value)

            return self.parse_postfix(expression)

        if token.type == "LBRACKET":
            expression = self.parse_list()
            return self.parse_postfix(expression)

        if token.type == "LBRACE":
            expression = self.parse_dict()
            return self.parse_postfix(expression)

        if token.type == "LPAREN":
            self.advance()

            expression = self.parse_expression()

            self.expect("RPAREN")

            return self.parse_postfix(expression)

        self.error(
            "expression invalide",
            token
        )

    def parse_postfix(self, expression):
        while True:
            if self.current().type == "LBRACKET":
                self.advance()

                index = self.parse_expression()

                self.expect("RBRACKET")

                expression = IndexAccess(
                    expression,
                    index
                )

                continue

            if self.current().type == "DOT":
                self.advance()

                name = self.expect("IDENTIFIER").value

                self.expect("LPAREN")

                arguments = []

                if self.current().type != "RPAREN":
                    while True:
                        arguments.append(self.parse_expression())

                        if self.current().type != "COMMA":
                            break

                        self.advance()

                self.expect("RPAREN")

                expression = MethodCall(
                    expression,
                    name,
                    arguments
                )

                continue

            break

        return expression

    def parse_index_access(self, expression):
        return self.parse_postfix(expression)

    def parse_list(self):
        self.expect("LBRACKET")

        elements = []

        self.skip_newlines()

        if self.current().type != "RBRACKET":
            while True:
                elements.append(self.parse_expression())

                self.skip_newlines()

                if self.current().type != "COMMA":
                    break

                self.advance()
                self.skip_newlines()

        self.expect("RBRACKET")

        return ListLiteral(elements)

    def parse_dict(self):
        self.expect("LBRACE")

        entries = []

        self.skip_newlines()

        if self.current().type != "RBRACE":
            while True:
                key = self.parse_expression()

                self.skip_newlines()

                self.expect("COLON")

                self.skip_newlines()

                value = self.parse_expression()

                entries.append((key, value))

                self.skip_newlines()

                if self.current().type != "COMMA":
                    break

                self.advance()
                self.skip_newlines()

        self.expect("RBRACE")

        return DictLiteral(entries)