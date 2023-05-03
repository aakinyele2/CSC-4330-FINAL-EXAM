import re

class Token:
    def __init__(self, token_type, value):
        self.type = token_type
        self.value = value

class Lexer:
    def __init__(self, input_string):
        self.input_string = input_string
        self.pos = 0
        self.tokens = []

    def skip_whitespace(self):
        while self.pos < len(self.input_string) and self.input_string[self.pos].isspace():
            self.pos += 1

    def match_pattern(self, pattern):
        match = re.match(pattern, self.input_string[self.pos:])
        if match:
            matched_string = match.group(0)
            self.tokens.append(Token(pattern, matched_string))
            self.pos += len(matched_string)
            return True
        return False

    def match_number(self):
        return self.match_pattern(r'\d+(\.\d+)?')

    def match_string_literal(self):
        if self.input_string[self.pos] == '"':
            escaped = False
            str_literal = ""
            for i in range(self.pos + 1, len(self.input_string)):
                if escaped:
                    str_literal += self.input_string[i]
                    escaped = False
                elif self.input_string[i] == '\\':
                    escaped = True
                elif self.input_string[i] == '"':
                    str_literal += self.input_string[i]
                    self.tokens.append(Token('string_literal', str_literal))
                    self.pos = i + 1
                    return True
                else:
                    str_literal += self.input_string[i]
            return False

    def match_char_literal(self):
        if self.input_string[self.pos] == "'":
            escaped = False
            char_literal = ""
            for i in range(self.pos + 1, len(self.input_string)):
                if escaped:
                    char_literal += self.input_string[i]
                    escaped = False
                elif self.input_string[i] == '\\':
                    escaped = True
                elif self.input_string[i] == "'":
                    char_literal += self.input_string[i]
                    self.tokens.append(Token('char_literal', char_literal))
                    self.pos = i + 1
                    return True
                else:
                    char_literal += self.input_string[i]
            return False

    def match_bool_literal(self):
        if self.match_pattern(r'(true|false)'):
            return True
        return False

    def tokenize(self):
        while self.pos < len(self.input_string):
            self.skip_whitespace()
            if self.match_number():
                continue
            elif self.match_string_literal():
                continue
            elif self.match_char_literal():
                continue
            elif self.match_bool_literal():
                continue
            else:
                # Unable to match any tokens, raise an exception
                raise Exception('Invalid token at position {}'.format(self.pos))

        return self.tokens
