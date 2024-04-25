'''
This module contains the classes that represent the nodes of the AST.
'''
from typing import Union
from tokens import TokenType

class Node:
    ''' 
    Node class is the base class for all the nodes in the AST.

    Methods:
    1. __init__: constructor method
    2. __repr__: representation method
    3. eval: method for evaluating the node
    '''
    def __init__(self) -> None:
        pass

    def __repr__(self) -> str:
        pass

    def eval(self):
        '''For actually evaluating the term, factor, or expression.'''

class BinaryOpNode(Node):
    '''
    BinaryOpNode class is a class that represents a binary operation node in the AST.

    Methods:
    1. __init__: constructor method
    2. __repr__: representation method
    3. eval: method for evaluating the node

    Parameters:
        type: TokenType
    
    # TODO: RETURN
    '''
    def __init__(self, ttype: TokenType) -> None:
        self.type: TokenType = ttype
        self.left: Node = None
        self.right: Node = None
        if ttype == TokenType.PLUS:
            self.func = lambda a,b : a+b
            self.symbol = '+'
        elif ttype == TokenType.MINUS:
            self.func = lambda a,b : a-b
            self.symbol = '-'
        elif ttype == TokenType.MULT:
            self.func = lambda a,b : int(a*b) if (a*b)%1 == 0 else a*b
            self.symbol = '*'
        elif ttype == TokenType.DIV:
            self.func = lambda a,b : a//b if a%b == 0 else a/b
            self.symbol = '/'

    def __repr__(self) -> str:
        return f'({self.left.__repr__()} {self.symbol} {self.right.__repr__()})'

    def eval(self):
        return self.func(self.left.eval(), self.right.eval())

class UnaryOpNode(Node):
    '''
    UnaryOpNode class is a class that represents a unary operation node in the AST.

    Methods:
    1. __init__: constructor method
    2. __repr__: representation method
    3. eval: method for evaluating the node

    Parameters:
        type: TokenType 
    '''
    def __init__(self, ttype: TokenType) -> None:
        self.type: TokenType = ttype
        self.child: Node = None
        if ttype == TokenType.MINUS:
            self.func = lambda a: -1*a
            self.symbol = '-'

    def __repr__(self) -> str:
        return f'({self.symbol}{self.child.__repr__()})'

    def eval(self):
        return self.func(self.child.eval())

class NumberNode(Node):
    '''
    NumberNode class is a class that represents a number node in the AST.
    
    Methods:
    1. __init__: constructor method
    2. __repr__: representation method
    3. eval: method for evaluating the node
    
    Parameters:
        value: Union[int,float]'''
    def __init__(self, value: Union[int,float]) -> None:
        self.value = value

    def __repr__(self) -> str:
        return f'{self.value}'

    def eval(self):
        return self.value

class IdentifierNode(Node):
    '''
    IdentifierNode class is a class that represents an identifier node in the AST.
    
    Methods:
    1. __init__: constructor method
    2. __repr__: representation method
    3. eval: method for evaluating the node
    
    Parameters:
        identifier: str
        value: Union[int,float]
    '''
    def __init__(self, identifier: str, value: Union[int,float]) -> None:
        self.value = value
        self.identifier = identifier

    def __repr__(self) -> str:
        return f'{self.identifier} -> {self.value}'

    def eval(self):
        return self.value

class BoolNode(Node):
    '''
    BoolNode class is a class that represents a boolean node in the AST.
    
    Methods:
    1. __init__: constructor method
    2. __repr__: representation method
    3. eval: method for evaluating the node
    
    Parameters:
        value: bool
    '''
    def __init__(self, ttype: TokenType) -> None:
        self.left: Node = None
        self.right: Node = None
        if ttype == TokenType.GREATER:
            self.func = lambda a,b : a>b
            self.symbol = '>'
        elif ttype == TokenType.LESS:
            self.func = lambda a,b : a<b
            self.symbol = '<'
        elif ttype == TokenType.GREATEREQ:
            self.func = lambda a,b : a>=b
            self.symbol = '>='
        elif ttype == TokenType.LESSEQ:
            self.func = lambda a,b : a<=b
            self.symbol = '<='
        elif ttype == TokenType.TWOEQ:
            self.func = lambda a,b : a==b
            self.symbol = '=='
        elif ttype == TokenType.OR:
            self.func = lambda a,b : a or b
            self.symbol = '||'
        elif ttype == TokenType.AND:
            self.func = lambda a,b : a and b
            self.symbol = '&&'

    def __repr__(self) -> str:
        return f'({self.left.__repr__()} {self.symbol} {self.right.__repr__()})'

    def eval(self):
        return self.func(self.left.eval(), self.right.eval())

class BoolLiteralNode(Node):
    '''
    BoolLiteralNode class is a class that represents a boolean literal node in the AST.
    
    Methods:
    1. __init__: constructor method
    2. __repr__: representation method
    3. eval: method for evaluating the node
    
    Parameters:
        value: bool
    '''
    def __init__(self, value: bool) -> None:
        self.value = value

    def __repr__(self) -> str:
        return f'{self.value}'

    def eval(self):
        return self.value
