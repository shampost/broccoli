from tokens import TokenType

class Parser():
    def __init__(self, tokens):
        self.tokens = tokens
        self.current_token = self.tokens[0] if self.tokens else None
        self.parser_token = []
        self.pos = 0

    def advance(self, by: int = 1):
        self.tokens.pop(0) # I have no clue what is happening here... I found this online.
        self.current_token = self.tokens[0] if self.tokens else None

    def parse(self):
        res = self.expression()
        return res 
    
    # ? Should this method perform token recovery in case there a missing token? Is that possible?
    def error(self):
        raise Exception('Invalid Syntax')

    def factor(self):
        token = self.current_token

        if token.type in (TokenType.INT, TokenType.FLOAT):
            self.advance()
            return NumberNode(token)

    def term(self):
        return self.bin_op(self.factor, (TokenType.MULT, TokenType.DIV))

    def expression(self):
        return self.bin_op(self.term, (TokenType.PLUS, TokenType.MINUS))

    def bin_op(self, func, ops):
        left = func()

        while self.current_token is not None and self.current_token.type in ops:
            op_token = self.current_token
            self.advance()
            right = func()
            left = BinOpNode(left, op_token, right)
        
        return left

#Nodes:
class NumberNode:
    def __init__(self, token) -> None:
        self.token = token
    
    def __repr__(self) -> str:
        return f'{self.token}'

class BinOpNode:
    def __init__(self, left_node, op_token, right_node) -> None:
       self.left_node = left_node
       self.right_node = right_node
       self.op_token = op_token

    def __repr__(self) -> str:
        return f'({self.left_node}, {self.op_token}, {self.right_node})'