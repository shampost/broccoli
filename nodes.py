from typing import Union
from tokens import TokenType

class Node:
    def __init__(self) -> None:
        pass

    def __repr__(self) -> str:
        pass

    def eval(self): 
        '''For actually evaluating the term, factor, or expression.'''
        pass

class BinaryOpNode(Node):
    def __init__(self, type: TokenType) -> None:
        super().__init__()
        self.type: TokenType = type
        self.left: Node = None
        self.right: Node = None
        if type == TokenType.PLUS:
            self.func = lambda a,b : a+b 
            self.symbol = '+'
        elif type == TokenType.MINUS:
            self.func = lambda a,b : a-b
            self.symbol = '-'
        elif type == TokenType.MULT:
            self.func = lambda a,b : a*b
            self.symbol = '*'
        elif type == TokenType.DIV:
            self.func = lambda a,b : a/b
            self.symbol = '/'

    def __repr__(self) -> str:
        return f'({self.left.__repr__()} {self.symbol} {self.right.__repr__()})'
        
    def eval(self):
        return self.func(self.left.eval(), self.right.eval())

class UnaryOpNode(Node):
    def __init__(self, type: TokenType) -> None:
        super().__init__()
        self.type: TokenType = type
        self.child: Node = None
        if type == TokenType.MINUS:
            self.func = lambda a: -1*a
            self.symbol = '-'

    def __repr__(self) -> str:
        return f'({self.symbol}{self.child.__repr__()})'

    def eval(self):
        return self.func(self.child.eval())

class NumberNode(Node):
    def __init__(self, value: Union[int,float]) -> None:
        super().__init__()
        self.value = value

    def __repr__(self) -> str:
        return f'{self.value}'

    def eval(self):
        return self.value




