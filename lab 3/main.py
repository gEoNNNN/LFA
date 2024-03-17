import re

# Define token types
token_patterns = [
    ('STRING', r'"(?:\\.|[^"])*"'),   # Matches strings
    ('NUMBER', r'-?(?:0|[1-9]\d*)(?:\.\d+)?(?:[eE][+-]?\d+)?'),  # Matches numbers
    ('TRUE', r'true'),                 # Matches true
    ('FALSE', r'false'),               # Matches false
    ('NULL', r'null'),                 # Matches null
    ('LBRACE', r'\{'),                 # Matches left brace
    ('RBRACE', r'\}'),                 # Matches right brace
    ('LSQUARE', r'\['),                # Matches left square bracket
    ('RSQUARE', r'\]'),                # Matches right square bracket
    ('COLON', r':'),                   # Matches colon
    ('COMMA', r','),                   # Matches comma
    ('WHITESPACE', r'\s+'),            # Matches whitespace
]

# Lexer class
class Lexer:
    def __init__(self, token_patterns):
        self.token_regex = re.compile('|'.join('(?P<%s>%s)' % pair for pair in token_patterns))

    def tokenize(self, code):
        for match in self.token_regex.finditer(code):
            token_type = match.lastgroup
            token_value = match.group()
            if token_type != 'WHITESPACE':
                yield token_type, token_value

# Example usage
lexer = Lexer(token_patterns)
json_text = '{"key": "value", "array": [1, 2, 3], "nested": {"inner_key": "inner_value"}}'
tokens = list(lexer.tokenize(json_text))
for token in tokens:
    print(token)
