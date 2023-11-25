from tokens import TokenType, Token
from nodes import Node, NumberNode, BinaryOpNode, UnaryOpNode


class Parser():
    def __init__(self, tokenList: list[Token]) -> None:
        self.pos = 0
        self.tokenList = tokenList
        self.rootNode: Node = None
        self.currentToken = self.tokenList[0]

    def showInput(self):
        print(self.rootNode)
    
    def evaluate(self):
        return self.rootNode.eval()

    def advance(self, by: int = 1):
        self.pos += by
        if self.pos < len(self.tokenList):
            self.currentToken = self.tokenList[self.pos]

    def parse(self):
        '''Uses grammar functions to parse input and set the rootNode'''
        try:
            self.rootNode = self.parseE()
        except SyntaxError as e:
            return e
        if self.currentToken != self.tokenList[-1]:
            raise SyntaxError()


##################################################################
########################## GRAMMAR ###############################
##################################################################
    def parseF(self) -> Node:
        # F -> Number | -F
        if self.currentToken.type == TokenType.INT:
            return NumberNode(value=int(self.currentToken.value))
        elif self.currentToken.type == TokenType.FLOAT:
            return NumberNode(value=float(self.currentToken.value))
        elif self.currentToken.type == TokenType.MINUS:
            node = UnaryOpNode(type=TokenType.MINUS)
            self.advance()
            node.child = self.parseF()
            return node
        #Add more grammar rules here
        raise SyntaxError()
        

    def parseT(self) -> Node:
        # T -> F * T | F / T | F
        F = self.parseF()
        self.advance()
        if self.currentToken.type == TokenType.MULT:
            node = BinaryOpNode(type=TokenType.MULT)
            node.left = F
            self.advance()
            node.right = self.parseT()
            return node
        elif self.currentToken.type == TokenType.DIV:
            node = BinaryOpNode(type=TokenType.DIV)
            node.left = F
            self.advance()
            node.right = self.parseT()
            return node
        self.advance(by=-1)
        return F

    def parseE(self) -> Node:
        # E -> T + E | T - E | T
        T = self.parseT()
        self.advance()
        if self.currentToken.type == TokenType.PLUS:
            node = BinaryOpNode(type=TokenType.PLUS)
            node.left = T
            self.advance()
            node.right = self.parseE()
            return node
        elif self.currentToken.type == TokenType.MINUS:
            node = BinaryOpNode(type=TokenType.MINUS)
            node.left = T
            self.advance()
            node.right = self.parseE()
            return node
        self.advance(by=-1)
        return T


myParser = Parser([Token(TokenType.MINUS), Token(TokenType.INT, 4)])
myParser.parse()
print(myParser.rootNode)
print(myParser.evaluate())

# print(myParser.currentToken)
# print(myParser.currentToken)
# print(myParser.currentToken)

# myParser.advance()

# print(myParser.currentToken)

# myParser.advance()

# print(myParser.currentToken)
# print(myParser.currentToken)
