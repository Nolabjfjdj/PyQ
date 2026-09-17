from dataclasses import dataclass


@dataclass
class Token:
    type: str
    value: str
    position: int


class Lexer:
    def __init__(self, source: str):
        self.source = source
        self.position = 0

    def tokenize(self):
        tokens = []

        while self.position < len(self.source):
            char = self.source[self.position]

            if char.isspace():
                self.position += 1
                continue

            if char == "(":
                tokens.append(Token("LPAREN", "(", self.position))
                self.position += 1
                continue

            if char == ")":
                tokens.append(Token("RPAREN", ")", self.position))
                self.position += 1
                continue

            if char == "=":
                if self._peek("="):
                    tokens.append(Token("EQUALS_EQUALS", "==", self.position))
                    self.position += 2
                else:
                    tokens.append(Token("EQUALS", "=", self.position))
                    self.position += 1
                continue

            if char == "!":
                if self._peek("="):
                    tokens.append(Token("NOT_EQUALS", "!=", self.position))
                    self.position += 2
                    continue

                raise SyntaxError(
                    f"Caractère inattendu à la position {self.position}: !"
                )

            if char == ">":
                if self._peek("="):
                    tokens.append(Token("GREATER_EQUALS", ">=", self.position))
                    self.position += 2
                else:
                    tokens.append(Token("GREATER", ">", self.position))
                    self.position += 1
                continue

            if char == "<":
                if self._peek("="):
                    tokens.append(Token("LESS_EQUALS", "<=", self.position))
                    self.position += 2
                else:
                    tokens.append(Token("LESS", "<", self.position))
                    self.position += 1
                continue

            if char == "+":
                tokens.append(Token("PLUS", "+", self.position))
                self.position += 1
                continue

            if char == "-":
                tokens.append(Token("MINUS", "-", self.position))
                self.position += 1
                continue

            if char == "*":
                tokens.append(Token("STAR", "*", self.position))
                self.position += 1
                continue

            if char == "/":
                tokens.append(Token("SLASH", "/", self.position))
                self.position += 1
                continue

            if char == '"':
                tokens.append(self._read_string())
                continue

            if char.isdigit():
                tokens.append(self._read_number())
                continue

            if char.isalpha() or char == "_":
                tokens.append(self._read_identifier())
                continue

            raise SyntaxError(
                f"Caractère inattendu à la position {self.position}: {char}"
            )

        tokens.append(Token("EOF", "", self.position))
        return tokens

    def _peek(self, expected):
        next_position = self.position + 1

        return (
            next_position < len(self.source)
            and self.source[next_position] == expected
        )

    def _read_string(self):
        start = self.position
        self.position += 1

        value = ""

        while self.position < len(self.source):
            char = self.source[self.position]

            if char == '"':
                self.position += 1
                return Token("STRING", value, start)

            value += char
            self.position += 1

        raise SyntaxError("Chaîne de caractères non terminée")

    def _read_number(self):
        start = self.position

        while (
            self.position < len(self.source)
            and self.source[self.position].isdigit()
        ):
            self.position += 1

        value = self.source[start:self.position]

        return Token("NUMBER", value, start)

    def _read_identifier(self):
        start = self.position

        while (
            self.position < len(self.source)
            and (
                self.source[self.position].isalnum()
                or self.source[self.position] == "_"
            )
        ):
            self.position += 1

        value = self.source[start:self.position]

        return Token("IDENTIFIER", value, start)