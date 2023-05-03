class Parser:
    def __init__(self, tokens):
        self.tokens = tokens
        self.current_token = None
        self.token_index = -1
        self.advance()

    def advance(self):
        self.token_index += 1
        if self.token_index < len(self.tokens):
            self.current_token = self.tokens[self.token_index]
        else:
            self.current_token = None

    def parse(self):
        parse_tree = self.program()
        if self.current_token is not None:
            raise Exception("Unexpected token at end of input")
        return parse_tree

    # Grammar Rules

    def program(self):
        parse_tree = Node("program")
        while self.current_token is not None:
            statement_node = self.statement()
            parse_tree.add_child(statement_node)
        return parse_tree

    def statement(self):
        if self.current_token.type == TokenType.KEYWORD:
            if self.current_token.value == "for":
                return self.for_loop_statement()
            elif self.current_token.value == "if":
                return self.if_statement()
            else:
                raise Exception("Invalid keyword")
        elif self.current_token.type == TokenType.IDENTIFIER:
            if self.tokens[self.token_index + 1].type == TokenType.ASSIGN:
                return self.assignment_statement()
            else:
                return self.function_call()
        else:
            raise Exception("Invalid statement")

    def for_loop_statement(self):
        parse_tree = Node("for_loop_statement")
        self.consume(TokenType.KEYWORD, "for")
        self.consume(TokenType.SYMBOL, "(")
        parse_tree.add_child(self.variable_declaration())
        self.consume(TokenType.SYMBOL, ";")
        parse_tree.add_child(self.expression())
        self.consume(TokenType.SYMBOL, ";")
        parse_tree.add_child(self.expression())
        self.consume(TokenType.SYMBOL, ")")
        parse_tree.add_child(self.code_block())
        return parse_tree

    def if_statement(self):
        parse_tree = Node("if_statement")
        self.consume(TokenType.KEYWORD, "if")
        self.consume(TokenType.SYMBOL, "(")
        parse_tree.add_child(self.expression())
        self.consume(TokenType.SYMBOL, ")")
        parse_tree.add_child(self.code_block())
        if self.current_token is not None and \
                self.current_token.type == TokenType.KEYWORD and self.current_token.value == "else":
            self.advance()
            parse_tree.add_child(self.code_block())
        return parse_tree

    def assignment_statement(self):
        parse_tree = Node("assignment_statement")
        parse_tree.add_child(Node(self.current_token.value))
        self.advance()
        self.consume(TokenType.ASSIGN, "=")
        parse_tree.add_child(self.expression())
        self.consume(TokenType.SYMBOL, ";")
        return parse_tree

    def variable_declaration(self):
        parse_tree = Node("variable_declaration")
        parse_tree.add_child(Node(self.current_token.value))
        self.advance()
        self.consume(TokenType.KEYWORD, "as")
        parse_tree.add_child(Node(self.current_token.value))
        self.advance()
        if self.current_token is not None and \
                self.current_token.type == TokenType.ASSIGN:
            self.advance()
            parse_tree.add_child(self.expression())
        return parse_tree
