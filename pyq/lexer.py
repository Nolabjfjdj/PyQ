class Token:
    def __init__(self, type_, value, position):
        self.type = type_
        self.value = value
        self.position = position

    def __repr__(self):
        return f"Token({self.type}, {self.value!r})"


class Lexer:
    def __init__(self, source):
        self.source = source
        self.tokens = []
        self.indentation_stack = [0]

    def tokenize(self):
        lines = self.source.splitlines()

        for line_number, line in enumerate(lines, start=1):
            stripped = line.lstrip()

            if not stripped:
                self.tokens.append(
                    Token("NEWLINE", "\n", line_number)
                )
                continue

            if stripped.startswith("#"):
                self.tokens.append(
                    Token("NEWLINE", "\n", line_number)
                )
                continue

            indentation = len(line) - len(stripped)

            if indentation > self.indentation_stack[-1]:
                self.indentation_stack.append(indentation)
                self.tokens.append(
                    Token("INDENT", indentation, line_number)
                )

            elif indentation < self.indentation_stack[-1]:
                while (
                    indentation < self.indentation_stack[-1]
                ):
                    self.indentation_stack.pop()
                    self.tokens.append(
                        Token("DEDENT", indentation, line_number)
                    )

                if indentation != self.indentation_stack[-1]:
                    raise SyntaxError(
                        f"Indentation invalide à la ligne {line_number}"
                    )

            i = indentation

            while i < len(line):
                char = line[i]

                if char == "#":
                    break

                if char.isspace():
                    i += 1
                    continue

                if char == '"':
                    start = i
                    i += 1
                    value = ""

                    while i < len(line):
                        if line[i] == '"':
                            break

                        value += line[i]
                        i += 1

                    if i >= len(line):
                        raise SyntaxError(
                            f"Chaîne non terminée à la ligne {line_number}"
                        )

                    i += 1

                    self.tokens.append(
                        Token("STRING", value, line_number)
                    )

                    continue

                if char.isdigit():
                    start = i

                    while (
                        i < len(line)
                        and line[i].isdigit()
                    ):
                        i += 1

                    value = line[start:i]

                    self.tokens.append(
                        Token("NUMBER", value, line_number)
                    )

                    continue

                if char.isalpha() or char == "_":
                    start = i

                    while (
                        i < len(line)
                        and (
                            line[i].isalnum()
                            or line[i] == "_"
                        )
                    ):
                        i += 1

                    value = line[start:i]

                    self.tokens.append(
                        Token(
                            "IDENTIFIER",
                            value,
                            line_number
                        )
                    )

                    continue

                if line.startswith("==", i):
                    self.tokens.append(
                        Token("EQUALS_EQUALS", "==", line_number)
                    )
                    i += 2
                    continue

                if line.startswith("!=", i):
                    self.tokens.append(
                        Token("NOT_EQUALS", "!=", line_number)
                    )
                    i += 2
                    continue

                if line.startswith(">=", i):
                    self.tokens.append(
                        Token("GREATER_EQUALS", ">=", line_number)
                    )
                    i += 2
                    continue

                if line.startswith("<=", i):
                    self.tokens.append(
                        Token("LESS_EQUALS", "<=", line_number)
                    )
                    i += 2
                    continue

                single_char_tokens = {
                    "=": "EQUALS",
                    ">": "GREATER",
                    "<": "LESS",
                    "+": "PLUS",
                    "-": "MINUS",
                    "*": "STAR",
                    "/": "SLASH",
                    ":": "COLON",
                    "(": "LPAREN",
                    ")": "RPAREN",
                    "[": "LBRACKET",
                    "]": "RBRACKET",
                    ",": "COMMA",
                }

                if char in single_char_tokens:
                    self.tokens.append(
                        Token(
                            single_char_tokens[char],
                            char,
                            line_number
                        )
                    )
                    i += 1
                    continue

                raise SyntaxError(
                    f"Caractère inattendu '{char}' "
                    f"à la ligne {line_number}"
                )

            self.tokens.append(
                Token("NEWLINE", "\n", line_number)
            )

        while len(self.indentation_stack) > 1:
            self.indentation_stack.pop()
            self.tokens.append(
                Token("DEDENT", 0, len(lines))
            )

        self.tokens.append(
            Token("EOF", None, len(lines))
        )

        return self.tokens