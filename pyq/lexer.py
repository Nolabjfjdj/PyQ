class Token:
    def __init__(self, type, value=None, position=0):
        self.type = type
        self.value = value
        self.position = position

    def __repr__(self):
        return f"Token({self.type!r}, {self.value!r}, {self.position})"


class Lexer:
    def __init__(self, source):
        self.source = source
        self.tokens = []
        self.indentation_stack = [0]
        self.bracket_depth = 0

    def tokenize(self):
        lines = self.source.splitlines()

        for line_number, line in enumerate(lines, start=1):
            stripped = line.lstrip(" ")

            if not stripped:
                if self.bracket_depth == 0:
                    self.tokens.append(
                        Token("NEWLINE", position=line_number)
                    )
                continue

            if stripped.startswith("#"):
                if self.bracket_depth == 0:
                    self.tokens.append(
                        Token("NEWLINE", position=line_number)
                    )
                continue

            indentation = len(line) - len(stripped)

            if self.bracket_depth == 0:
                if indentation > self.indentation_stack[-1]:
                    self.indentation_stack.append(indentation)
                    self.tokens.append(
                        Token("INDENT", position=line_number)
                    )

                elif indentation < self.indentation_stack[-1]:
                    while indentation < self.indentation_stack[-1]:
                        self.indentation_stack.pop()
                        self.tokens.append(
                            Token("DEDENT", position=line_number)
                        )

                    if indentation != self.indentation_stack[-1]:
                        raise SyntaxError(
                            f"Indentation invalide à la ligne {line_number}"
                        )

            self.tokenize_line(stripped, line_number)

            if self.bracket_depth == 0:
                self.tokens.append(
                    Token("NEWLINE", position=line_number)
                )

        while len(self.indentation_stack) > 1:
            self.indentation_stack.pop()
            self.tokens.append(
                Token("DEDENT", position=len(lines) + 1)
            )

        if self.bracket_depth != 0:
            raise SyntaxError(
                "Structure entre crochets ou accolades non terminée"
            )

        self.tokens.append(
            Token("EOF", position=len(lines) + 1)
        )

        return self.tokens

    def tokenize_line(self, line, line_number):
        i = 0

        while i < len(line):
            char = line[i]

            if char == " " or char == "\t":
                i += 1
                continue

            if char == "#":
                break

            if char == '"':
                i += 1
                value = ""

                while i < len(line) and line[i] != '"':
                    value += line[i]
                    i += 1

                if i >= len(line):
                    raise SyntaxError(
                        f"Chaîne non terminée à la ligne {line_number}"
                    )

                i += 1

                self.tokens.append(
                    Token(
                        "STRING",
                        value,
                        line_number
                    )
                )

                continue

            if char.isdigit():
                start = i

                while i < len(line) and line[i].isdigit():
                    i += 1

                if (
                    i < len(line)
                    and line[i] == "."
                    and i + 1 < len(line)
                    and line[i + 1].isdigit()
                ):
                    i += 1

                    while i < len(line) and line[i].isdigit():
                        i += 1

                value = line[start:i]

                self.tokens.append(
                    Token(
                        "NUMBER",
                        value,
                        line_number
                    )
                )

                continue

            if char.isalpha() or char == "_":
                start = i
                i += 1

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

            single_tokens = {
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
                "{": "LBRACE",
                "}": "RBRACE",
                ",": "COMMA",
                ".": "DOT",
            }

            if char in single_tokens:
                token_type = single_tokens[char]

                self.tokens.append(
                    Token(
                        token_type,
                        char,
                        line_number
                    )
                )

                if char in "([{":
                    self.bracket_depth += 1

                elif char in ")]}":
                    self.bracket_depth -= 1

                    if self.bracket_depth < 0:
                        raise SyntaxError(
                            f"Structure fermante inattendue à la ligne {line_number}"
                        )

                i += 1
                continue

            raise SyntaxError(
                f"Caractère inattendu '{char}' à la ligne {line_number}"
            ) 