import re
import enum
from graphviz import Digraph

class TokenType(enum.Enum):
    WHITESPACE = 1
    STRING = 2
    NUMBER = 3
    BOOLEAN = 4
    NULL = 5
    BRACE_OPEN = 6
    BRACE_CLOSE = 7
    BRACKET_OPEN = 8
    BRACKET_CLOSE = 9
    COLON = 10
    COMMA = 11

def lexer(json):
    tokens = []
    token_regex = r'\s+|"(?:\\.|[^"\\])*"|[-+]?\d*\.?\d+([eE][-+]?\d+)?|true|false|null|[\[\]{}:,\s]'
    for match in re.finditer(token_regex, json):
        value = match.group(0).strip()
        if value:
            if value == '{':
                tokens.append((TokenType.BRACE_OPEN, value))
            elif value == '}':
                tokens.append((TokenType.BRACE_CLOSE, value))
            elif value == '[':
                tokens.append((TokenType.BRACKET_OPEN, value))
            elif value == ']':
                tokens.append((TokenType.BRACKET_CLOSE, value))
            elif value == ':':
                tokens.append((TokenType.COLON, value))
            elif value == ',':
                tokens.append((TokenType.COMMA, value))
            elif value in ('true', 'false'):
                tokens.append((TokenType.BOOLEAN, value))
            elif value == 'null':
                tokens.append((TokenType.NULL, value))
            elif value.startswith('"'):
                tokens.append((TokenType.STRING, value[1:-1]))
            else:
                tokens.append((TokenType.NUMBER, value))
    return tokens

class ASTNode:
    def __init__(self, type, children=None, value=None):
        self.type = type
        self.value = value
        self.children = children if children is not None else []

    def __repr__(self):
        type_name = self.type.name if isinstance(self.type, enum.Enum) else self.type
        return f"{type_name}({self.value}, {self.children})"

def parse(tokens):
    root = ASTNode(TokenType.BRACE_OPEN, value="ROOT")
    current_node = root
    stack = [root]

    for token_type, value in tokens:
        if token_type == TokenType.BRACE_OPEN or token_type == TokenType.BRACKET_OPEN:
            node = ASTNode(token_type, value=value)
            current_node.children.append(node)
            stack.append(node)
            current_node = node
        elif token_type == TokenType.BRACE_CLOSE or token_type == TokenType.BRACKET_CLOSE:
            stack.pop()
            current_node = stack[-1]
        elif token_type in (TokenType.STRING, TokenType.NUMBER, TokenType.BOOLEAN, TokenType.NULL):
            node = ASTNode(token_type, value=value)
            current_node.children.append(node)

    return root

def add_nodes_edges(tree, graph=None):
    if graph is None:
        graph = Digraph()
        graph.node(name=str(id(tree)), label=f'{tree.type.name}({tree.value})')

    for child in tree.children:
        child_label = f'{child.type.name}({child.value})' if child.value else child.type.name
        graph.node(name=str(id(child)), label=child_label)
        graph.edge(str(id(tree)), str(id(child)))
        graph = add_nodes_edges(child, graph)

    return graph

with open('example.json', 'r') as file:
    json_content = file.read()

tokens = lexer(json_content)
ast = parse(tokens)
graph = add_nodes_edges(ast)
graph.render('ast', view=True)
