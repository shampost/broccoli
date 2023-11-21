from typing import Union

class Node:
    def __init__(self) -> None:
        pass

    def __repr__(self) -> str:
        pass

    def eval(self): 
        '''For actually evaluating the term, factor, or expression.'''
        pass

class InfixOpNode(Node):
    def __init__(self, type: str) -> None:
        super().__init__()
        self.type: str = type
        self.left: Node = None
        self.right: Node = None
        if type == '+':
            self.func = lambda a,b : a+b 
        elif type == '-':
            self.func = lambda a,b : a-b
        elif type == '*':
            self.func = lambda a,b : a*b
        elif type == '/':
            self.func = lambda a,b : a/b

    def __repr__(self) -> str:
        return f'({self.left.__repr__()} {self.type} {self.right.__repr__()})'
        
    def eval(self):
        return self.func(self.left.eval(), self.right.eval)

class PrefixOpNode(Node):
    def __init__(self, type: str) -> None:
        super().__init__()
        self.type: str = type
        self.child: Node = None
        if type == "-":
            self.func = lambda a: -1*a

    def __repr__(self) -> str:
        return f'({self.type} {self.child.__repr__()})'

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




