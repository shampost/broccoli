'''
Parser
'''
from tokens import TokenType, Token
from nodes import Node, NumberNode, BinaryOpNode, UnaryOpNode,\
                  IdentifierNode, BoolNode, BoolLiteralNode
from errors import InvalidRedeclaration
from memory import Memory

class Parser():
    # write docstring

    def __init__(self, memory: Memory) -> None:
        self.pos = 0
        self.lineTokenList = []
        self.allTokensList = None
        self.rootNode: Node = None
        self.currentToken: Token = None
        self.memory = memory
        self.currentLine = None

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
        i = 0
        while i < len(self.allTokensList):
            self.lineTokenList = self.allTokensList[i] 
            self.pos = 0
            self.currentToken = self.lineTokenList[0]
            #try:
            self.rootNode = self.parseLine()
            if isinstance(self.rootNode, BoolNode):
                if self.lineTokenList[0].type == TokenType.IF:
                    if_block_tokens = []
                    for j in range(i+1,len(self.allTokensList)):
                        types = [token.type for token in self.allTokensList[j]]
                        if TokenType.RCURL in types:
                            i = j
                            break
                        if_block_tokens.append(self.allTokensList[j])
                    if self.rootNode.eval():
                        #return node from if block
                        if_parser = Parser(self.memory)
                        if_parser.setTokens(if_block_tokens)
                        if_parser.parse()
                        self.rootNode = if_parser.rootNode
                else:
                    if_block_tokens = []
                    for j in range(i+1,len(self.allTokensList)):
                        types = [token.type for token in self.allTokensList[j]]
                        if TokenType.RBRACKET in types:
                            i = j
                            break
                        if_block_tokens.append(self.allTokensList[j])
                    while self.rootNode.eval():
                        #return node from if block
                        if_parser = Parser(self.memory)
                        if_parser.setTokens(if_block_tokens)
                        if_parser.parse()
                        self.rootNode = if_parser.rootNode
                ifBlockTokens = []
                for j in range(i+1,len(self.allTokensList)):
                   
                    types = map(lambda token: token.type, self.allTokensList[j])
                    if TokenType.RCURL in types:
                        i = j
                        break
                    ifBlockTokens.append(self.allTokensList[j])
                if self.rootNode.eval():
                    #return node from if block
                    ifParser = Parser(self.memory)
                    ifParser.setTokens(ifBlockTokens)
                    ifParser.parse()
                    self.rootNode = ifParser.rootNode
            #except SyntaxError as e:
                #return e
            # print(i)
            if self.currentToken != self.lineTokenList[-1]:
                raise SyntaxError()
            i += 1

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
            return self.parseIf()
        elif self.currentToken.type == TokenType.IF:
            return self.parseIf()
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
            if self.currentToken.value in self.memory.get_all().keys():
                return IdentifierNode(self.currentToken.value, self.memory.get_item(self.currentToken.value))
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
            if self.memory.get_item(identifier) is None:
                self.memory.add_item(identifier, value)
            else:
                raise InvalidRedeclaration(f'\n\nVariable \'{identifier}\' has already been declared. Please rename your variable\n')
            node = IdentifierNode(identifier=identifier, value=value)
        return node
    
    def parseRedeclare(self) -> Node:
        if self.memory.get_item(self.currentToken.value) is not None:
            identifier = self.currentToken.value
            self.advance(by=2)
            value = self.parseE().eval()
            self.memory.add_item(identifier, value)
            return IdentifierNode(identifier=identifier, value=value)
        else:
            raise SyntaxError()

    def parseWhile(self) -> Node:
        whileMem = []
        self.advance()
        whileExpBool = self.parseBoolE().eval()
        self.advance(by=1)
        while self.currentToken.type != TokenType.RBRACKET and whileExpBool:
            # whileMem = whileMem.append(self.currentToken)
            whileMem.append(self.currentToken)
            self.advance()
        boolParser = Parser(memory=self.memory)
        boolParser.setTokens(whileMem)
        boolParser.parse()
            
        # if self.currentToken.type == TokenType.LPAREN: 
        #     try:
        #         whileExpBool = self.parseBoolE().eval()
        #     except SyntaxError:
        #         print(f'Invalid Syntax')

    def parseIf(self) -> Node:
        self.advance()
        boolNode = self.parseBoolE()
        self.advance()
        if self.currentToken.type != TokenType.LCURL:
            raise SyntaxError()
        return boolNode
        
    
    def parseBoolE(self) -> BoolNode:
        # E -> T || E     T && E       !E        T
        T = self.parseBoolT()
        self.advance()
        if self.currentToken.type == TokenType.OR:
            node = BoolNode(type=TokenType.OR)
            node.left = T
            self.advance()
            node.right = self.parseBoolE()
            return node
        elif self.currentToken.type == TokenType.AND:
            node = BoolNode(type=TokenType.AND)
            node.left = T
            self.advance()
            node.right = self.parseBoolE()
            return node
        self.advance(by=-1)
        return T

    def parseBoolT(self) -> BoolNode:
        # T -> F == T     F < T     F <= T     F > T     F >= T     F
        F = self.parseBoolF()
        self.advance()
        if self.currentToken.type == TokenType.TWOEQ:
            node = BoolNode(type=TokenType.TWOEQ)
            node.left = F
            self.advance()
            node.right = self.parseBoolT()
            return node
        elif self.currentToken.type == TokenType.LESS:
            node = BoolNode(type=TokenType.LESS)
            node.left = F
            self.advance()
            node.right = self.parseBoolT()
            return node
        elif self.currentToken.type == TokenType.GREATER:
            node = BoolNode(type=TokenType.GREATER)
            node.left = F
            self.advance()
            node.right = self.parseBoolT()
            return node
        elif self.currentToken.type == TokenType.LESSEQ:
            node = BoolNode(type=TokenType.LESSEQ)
            node.left = F
            self.advance()
            node.right = self.parseBoolT()
            return node
        elif self.currentToken.type == TokenType.GREATEREQ:
            node = BoolNode(type=TokenType.GREATEREQ)
            node.left = F
            self.advance()
            node.right = self.parseBoolT()
            return node
        self.advance(by=-1)
        return F

    def parseBoolF(self) -> Node:
        # F -> Number     Identifier     !F      True       False 
        if self.currentToken.type == TokenType.LPAREN:
            self.advance()
            node = self.parseBoolE()
            self.advance()
            if self.currentToken.type != TokenType.RPAREN:
                raise SyntaxError()
            return node
        if self.currentToken.type == TokenType.INT:
            return NumberNode(value=int(self.currentToken.value))
        elif self.currentToken.type == TokenType.FLOAT:
            return NumberNode(value=float(self.currentToken.value))
        elif self.currentToken.type == TokenType.STR:
            if self.currentToken.value in self.memory.get_all().keys():
                return IdentifierNode(self.currentToken.value, self.memory.get_item(self.currentToken.value))
        elif self.currentToken.type == TokenType.MINUS:
            node = UnaryOpNode(type=TokenType.MINUS)
            self.advance()
            node.child = self.parseBoolF()
            return node
        elif self.currentToken.type == TokenType.TRUE:
            return BoolLiteralNode(value=True)
        elif self.currentToken.type == TokenType.FALSE:
            return BoolLiteralNode(value=False)
        elif self.currentToken.type == TokenType.NOT:
            self.advance()
            node = self.parseBoolF()
            if node.eval():
                return BoolLiteralNode(value=False)
            else:
                return BoolLiteralNode(value=True)
        #Add more grammar rules here
        raise SyntaxError()

# myParser = Parser([Token(TokenType.MINUS), Token(TokenType.INT, 4)])
# myParser.parse()
# print(myParser.rootNode)
# print(myParser.evaluate())
