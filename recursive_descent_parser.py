'''
Parser
'''
from tokens import TokenType, Token
from nodes import Node, NumberNode, BinaryOpNode, UnaryOpNode,\
                  IdentifierNode, BoolNode, BoolLiteralNode
from errors import InvalidRedeclaration
from memory import Memory

class Parser():
    '''
    Parser class is a class that parses
    the input and generates the AST.
    
    Methods:
    1. parse: method for parsing the input
    2. parseLine: method for parsing a line
    3. parseE: method for parsing an expression
    4. parseT: method for parsing a term
    5. parseF: method for parsing a factor
    6. parseId: method for parsing an identifier
    7. parseRedeclare: method for parsing a redeclaration
    8. parseWhile: method for parsing a while loop
    9. parseIf: method for parsing an if statement
    10. parseBoolE: method for parsing a boolean expression
    11. parseBoolT: method for parsing a boolean term
    12. parseBoolF: method for parsing a boolean factor
    
    Parameters:
        memory: Memory
    '''
    def __init__(self, memory: Memory) -> None:
        self.pos = 0
        self.line_token_list = []
        self.all_tokens_list = None
        self.root_node: Node = None
        self.current_token: Token = None
        self.memory = memory
        self.current_line = None

    def show_input(self):
        '''
        Prints the root node
        '''
        print(self.root_node)

    def evaluate(self):
        '''
        Evaluates the root node
        '''
        return self.root_node.eval()

    def advance(self, by: int = 1):
        '''
        Advances the current token by the given number of steps.
        '''
        self.pos += by
        if self.pos < len(self.line_token_list):
            self.current_token = self.line_token_list[self.pos]

    def set_tokens(self, token_list: list[Token]):
        '''
        Sets the tokens for the parser
        '''
        self.pos = 0
        self.all_tokens_list = token_list
        self.current_token = self.all_tokens_list[0][0]

    def parse(self):
        '''
        Uses grammar functions to parse input and set the rootNode
        '''
        i = 0
        while i < len(self.all_tokens_list):
            self.line_token_list = self.all_tokens_list[i]
            self.pos = 0
            self.current_token = self.line_token_list[0]
            #try:
            self.root_node = self.parse_line()
            if isinstance(self.root_node, BoolNode):
                if self.line_token_list[0].type == TokenType.IF:
                    if_block_tokens = []
                    for j in range(i+1,len(self.all_tokens_list)):
                        types = [token.type for token in self.all_tokens_list[j]]
                        if TokenType.RCURL in types:
                            i = j
                            break
                        if_block_tokens.append(self.all_tokens_list[j])
                    if self.root_node.eval():
                        #return node from if block
                        if_parser = Parser(self.memory)
                        if_parser.set_tokens(if_block_tokens)
                        if_parser.parse()
                        self.root_node = if_parser.root_node
                else:
                    if_block_tokens = []
                    for j in range(i+1,len(self.all_tokens_list)):
                        types = [token.type for token in self.all_tokens_list[j]]
                        if TokenType.RBRACKET in types:
                            i = j
                            break
                        if_block_tokens.append(self.all_tokens_list[j])
                    while self.root_node.eval():
                        #return node from if block
                        if_parser = Parser(self.memory)
                        if_parser.set_tokens(if_block_tokens)
                        if_parser.parse()
                        self.root_node = if_parser.root_node
            #except SyntaxError as e:
                #return e
            # print(i)
            if self.current_token != self.line_token_list[-1]:
                raise SyntaxError()
            i += 1

##################################################################
########################## GRAMMAR ###############################
##################################################################

    def parse_line(self) -> Node:
        '''
        S -> E | VariableDec
        '''

        if self.current_token.type == TokenType.ID:
            return self.parse_id()
        if len(self.line_token_list) > 1 and self.line_token_list[self.pos + 1].type == TokenType.EQUALS:
            return self.parse_redeclare()
        if self.current_token.type == TokenType.WHILE:
            return self.parse_if()
        if self.current_token.type == TokenType.IF:
            return self.parse_if()
        #################DANGER ZONE#####################
        if self.current_token.type == TokenType.PRINT:
            self.advance()
            print_node = self.pares_e()
            print(print_node.eval())
            return print_node
        #################################################
        return self.pares_e()

    def pares_e(self) -> Node:
        '''
        E -> T + E | T - E | T
        '''
        T = self.parse_t()
        self.advance()
        if self.current_token.type == TokenType.PLUS:
            node = BinaryOpNode(ttype=TokenType.PLUS)
            node.left = T
            self.advance()
            node.right = self.pares_e()
            return node
        if self.current_token.type == TokenType.MINUS:
            node = BinaryOpNode(ttype=TokenType.MINUS)
            node.left = T
            self.advance()
            node.right = self.pares_e()
            return node
        self.advance(by=-1)
        return T

    def parse_f(self) -> Node:
        '''
        F -> Number | identifier | -F
        '''
        if self.current_token.type == TokenType.LPAREN:
            self.advance()
            node = self.pares_e()
            self.advance()
            if self.current_token.type != TokenType.RPAREN:
                raise SyntaxError()
            return node
        if self.current_token.type == TokenType.INT:
            return NumberNode(value=int(self.current_token.value))
        if self.current_token.type == TokenType.FLOAT:
            return NumberNode(value=float(self.current_token.value))
        if self.current_token.type == TokenType.STR:
            if self.current_token.value in self.memory.get_all().keys():
                return IdentifierNode(self.current_token.value, self.memory.get_item(self.current_token.value))
        if self.current_token.type == TokenType.MINUS:
            node = UnaryOpNode(ttype=TokenType.MINUS)
            self.advance()
            node.child = self.parse_f()
            return node
        #Add more grammar rules here
        raise SyntaxError()

    def parse_t(self) -> Node:
        '''
        T -> F * T | F / T | F
        '''
        F = self.parse_f()
        self.advance()
        if self.current_token.type == TokenType.MULT:
            node = BinaryOpNode(ttype=TokenType.MULT)
            node.left = F
            self.advance()
            node.right = self.parse_t()
            return node
        if self.current_token.type == TokenType.DIV:
            node = BinaryOpNode(ttype=TokenType.DIV)
            node.left = F
            self.advance()
            node.right = self.parse_t()
            return node
        self.advance(by=-1)
        return F

    def parse_id(self) -> Node:
        '''
        let id = num
        '''
        if self.current_token.type == TokenType.ID:
            self.advance()
            identifier = self.current_token.value
            self.advance(by=2)
            value = self.pares_e().eval()
            if self.memory.get_item(identifier) is None:
                self.memory.add_item(identifier, value)
            else:
                raise InvalidRedeclaration(f'\n\nVariable \'{identifier}\' has already been declared. Please rename your variable\n')
            node = IdentifierNode(identifier=identifier, value=value)
        return node

    def parse_redeclare(self) -> Node:
        '''
        var id = num
        '''
        if self.memory.get_item(self.current_token.value) is not None:
            identifier = self.current_token.value
            self.advance(by=2)
            value = self.pares_e().eval()
            self.memory.add_item(identifier, value)
            return IdentifierNode(identifier=identifier, value=value)
        raise SyntaxError()

    def parse_while(self) -> Node:
        '''
        while (boolE) { S }
        '''
        while_mem = []
        self.advance()
        while_exp_bool = self.parse_bool_e().eval()
        self.advance(by=1)
        while self.current_token.type != TokenType.RBRACKET and while_exp_bool:
            # whileMem = whileMem.append(self.currentToken)
            while_mem.append(self.current_token)
            self.advance()
        bool_parser = Parser(memory=self.memory)
        bool_parser.set_tokens(while_mem)
        bool_parser.parse()

        # if self.currentToken.type == TokenType.LPAREN:
        #     try:
        #         whileExpBool = self.parseBoolE().eval()
        #     except SyntaxError:
        #         print(f'Invalid Syntax')

    def parse_if(self) -> Node:
        '''
        if (boolE) { S }
        '''
        self.advance()
        bool_node = self.parse_bool_e()
        self.advance()
        if self.current_token.type != TokenType.LCURL:
            raise SyntaxError()
        return bool_node

    def parse_bool_e(self) -> BoolNode:
        '''
        E -> T || E     T && E       !E        T
        '''
        T = self.parse_bool_t()
        self.advance()
        if self.current_token.type == TokenType.OR:
            node = BoolNode(ttype=TokenType.OR)
            node.left = T
            self.advance()
            node.right = self.parse_bool_e()
            return node
        if self.current_token.type == TokenType.AND:
            node = BoolNode(ttype=TokenType.AND)
            node.left = T
            self.advance()
            node.right = self.parse_bool_e()
            return node
        self.advance(by=-1)
        return T

    def parse_bool_t(self) -> BoolNode:
        '''
        T -> F == T     F < T     F <= T     F > T     F >= T     F
        '''
        F = self.parse_bool_f()
        self.advance()
        if self.current_token.type == TokenType.TWOEQ:
            node = BoolNode(ttype=TokenType.TWOEQ)
            node.left = F
            self.advance()
            node.right = self.parse_bool_t()
            return node
        if self.current_token.type == TokenType.LESS:
            node = BoolNode(ttype=TokenType.LESS)
            node.left = F
            self.advance()
            node.right = self.parse_bool_t()
            return node
        if self.current_token.type == TokenType.GREATER:
            node = BoolNode(ttype=TokenType.GREATER)
            node.left = F
            self.advance()
            node.right = self.parse_bool_t()
            return node
        if self.current_token.type == TokenType.LESSEQ:
            node = BoolNode(ttype=TokenType.LESSEQ)
            node.left = F
            self.advance()
            node.right = self.parse_bool_t()
            return node
        if self.current_token.type == TokenType.GREATEREQ:
            node = BoolNode(ttype=TokenType.GREATEREQ)
            node.left = F
            self.advance()
            node.right = self.parse_bool_t()
            return node
        self.advance(by=-1)
        return F

    def parse_bool_f(self) -> Node:
        '''
        F -> Number     Identifier     !F      True       False 
        '''
        if self.current_token.type == TokenType.LPAREN:
            self.advance()
            node = self.parse_bool_e()
            self.advance()
            if self.current_token.type != TokenType.RPAREN:
                raise SyntaxError()
            return node
        if self.current_token.type == TokenType.INT:
            return NumberNode(value=int(self.current_token.value))
        if self.current_token.type == TokenType.FLOAT:
            return NumberNode(value=float(self.current_token.value))
        if self.current_token.type == TokenType.STR:
            if self.current_token.value in self.memory.get_all().keys():
                return IdentifierNode(self.current_token.value, self.memory.get_item(self.current_token.value))
        if self.current_token.type == TokenType.MINUS:
            node = UnaryOpNode(ttype=TokenType.MINUS)
            self.advance()
            node.child = self.parse_bool_f()
            return node
        if self.current_token.type == TokenType.TRUE:
            return BoolLiteralNode(value=True)
        if self.current_token.type == TokenType.FALSE:
            return BoolLiteralNode(value=False)
        if self.current_token.type == TokenType.NOT:
            self.advance()
            node = self.parse_bool_f()
            if node.eval():
                return BoolLiteralNode(value=False)
            return BoolLiteralNode(value=True)
        #Add more grammar rules here
        raise SyntaxError()

# myParser = Parser([Token(TokenType.MINUS), Token(TokenType.INT, 4)])
# myParser.parse()
# print(myParser.rootNode)
# print(myParser.evaluate())
