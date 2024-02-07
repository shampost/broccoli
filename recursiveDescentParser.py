from tokens import TokenType, Token
from nodes import Node, NumberNode, BinaryOpNode, UnaryOpNode, IdentifierNode, BoolNode
from errors import InvalidRedeclaration
from memory import Memory
from lexer import Lexer

class Parser():
    def __init__(self, memory: Memory) -> None:
        self.pos = 0
        self.lineTokenList = []
        self.allTokensList = None
        self.rootNode: Node = None
        self.currentToken: Token = None
        self.memory = memory

    def showInput(self):
        print(self.rootNode)
    
    def evaluate(self):
        return self.rootNode.eval()

    def advance(self, by: int = 1):
        self.pos += by
        if self.pos < len(self.lineTokenList):
            self.currentToken = self.lineTokenList[self.pos]

    def setTokens(self, tokenList: list[Token]):
        self.pos = 0
        self.allTokensList = tokenList
        self.currentToken = self.allTokensList[0][0]

    def parse(self):
        '''Uses grammar functions to parse input and set the rootNode'''
        for i in range(len(self.allTokensList)):
            self.lineTokenList = self.allTokensList[i] 
            self.pos = 0 
            self.currentToken = self.lineTokenList[0]
            try:
                self.rootNode = self.parseLine()
            except SyntaxError as e:
                return e
            if self.currentToken != self.lineTokenList[-1]:
                raise SyntaxError()

##################################################################
########################## GRAMMAR ###############################
##################################################################

    def parseLine(self) -> Node:
        # S -> E | VariableDec
        
        if self.currentToken.type == TokenType.ID:
            return self.parseId()
        elif len(self.lineTokenList) > 1 and self.lineTokenList[self.pos + 1].type == TokenType.EQUALS:
            return self.parseRedeclare()
        elif self.currentToken.type == TokenType.WHILE:
            return self.parseWhile()
        else:
            return self.parseE()
            

    def parseF(self) -> Node:
        # F -> Number | identifier | -F
        if self.currentToken.type == TokenType.LPAREN:
            self.advance()
            node = self.parseE()
            self.advance()
            if self.currentToken.type != TokenType.RPAREN:
                raise SyntaxError()
            return node
        if self.currentToken.type == TokenType.INT:
            return NumberNode(value=int(self.currentToken.value))
        elif self.currentToken.type == TokenType.FLOAT:
            return NumberNode(value=float(self.currentToken.value))
        elif self.currentToken.type == TokenType.STR:
            if self.currentToken.value in self.memory.getAll().keys():
                return IdentifierNode(self.currentToken.value, self.memory.getItem(self.currentToken.value))
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

    def parseId(self) -> Node:
        #let id = num
        if self.currentToken.type == TokenType.ID:
            self.advance()
            identifier = self.currentToken.value
            self.advance(by=2)
            value = self.parseE().eval() 
            if self.memory.getItem(identifier) is None:
                self.memory.addItem(identifier, value)
            else:
                raise InvalidRedeclaration(f'\n\nVariable \'{identifier}\' has already been declared. Please rename your variable\n')
            node = IdentifierNode(identifier=identifier, value=value)
        return node
    
    def parseRedeclare(self) -> Node:
        if self.memory.getItem(self.currentToken.value) is not None:
            identifier = self.currentToken.value
            self.advance(by=2)
            value = self.parseE().eval()
            self.memory.addItem(identifier, value)
            return IdentifierNode(identifier=identifier, value=value)
        else:
            raise SyntaxError()

    def parseWhile(self) -> Node:
        self.advance()
        return self.parseBool()
    
    def parseBool(self) -> BoolNode:
        
        pass
# myParser = Parser([Token(TokenType.MINUS), Token(TokenType.INT, 4)])
# myParser.parse()
# print(myParser.rootNode)
# print(myParser.evaluate())
