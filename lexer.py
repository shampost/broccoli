from tokens import Token, TokenType

class Lexer:
    def __init__(self, text: str) -> None:
        self.text = text
        self.pos = 0
        self.tokens = []
        self.stack: list[Token] = []
        self.letters = ['a','b','c','d','e','f','g','h','i','j','k','l','m','n','o','p','q','r','s','t','u','v','w','x','y','z','A','B','C','D','E','F','G','H','I','J','K','L','M','N','O','P','Q','R','S','T','U','V','W','X','Y','Z']
        self.numbers = ['0','1','2','3','4','5','6','7','8','9']
    def __repr__(self) -> str:
        return self.tokens
    
    def advance(self):
        token = None
        current_char = self.text[self.pos]

        if current_char == " ":
            self.pos += 1
            return 

        #Push to stack
        if current_char == "+":
            token = Token(TokenType.PLUS, "+") 
        elif current_char == "-":
            token = Token(TokenType.MINUS, "-") 
        elif current_char == "*":
            token = Token(TokenType.MULT, "*")
        elif current_char == "/":
            token = Token(TokenType.DIV, "/")
        elif current_char == "(":
            token = Token(TokenType.LPAREN, "(") 
            self.stack.append(token)
        elif current_char == ")":
            token = Token(TokenType.RPAREN, ")")
            if self.stack.pop().type != TokenType.LPAREN: 
                raise SyntaxError()
        elif current_char == "{":
            token = Token(TokenType.LCURL, "{")
            self.stack.append(token)
        elif current_char == "}":
            token = Token(TokenType.RCURL, "}")
            if self.stack.pop().type != TokenType.LCURL: 
                raise SyntaxError()
        elif current_char == "[":
            token = Token(TokenType.LBRACKET, "[")
            self.stack.append(token)
        elif current_char == ")":
            token = Token(TokenType.RBRACKET, "]")
            if self.stack.pop().type != TokenType.LBRACKET: 
                raise SyntaxError()
        elif current_char in self.numbers:
            token = Token(TokenType.INT, current_char)
        elif current_char in self.letters:
            token = Token(TokenType.STR, current_char)

        self.tokens.append(token)
        self.pos += 1

    def combine(self, tokList: list[Token]):
        #combines consecutive number or letter tokens into one token
        newTokList: list[Token] = []
        allOneToken = ""

        for i,tok in enumerate(tokList):
            if i == 0:
                currentType: TokenType = tok.type
                allOneToken += tok.value
                continue
            lastType: TokenType = currentType
            currentType: TokenType = tok.type

            if currentType == lastType:
                allOneToken += tok.value
            else:
                newTokList.append(Token(lastType, allOneToken))
                allOneToken = tok.value
            
            if i == len(tokList) - 1:
                newTokList.append(Token(currentType, allOneToken))
        
        self.tokens = newTokList

    def tokenize(self) -> list[Token]:
        while self.pos != len(self.text):
            self.advance()
        self.combine(self.tokens)
        if self.stack:
            raise SyntaxError()
        return self.tokens

lexer = Lexer("my expression is (19 + (12-4))")

print(lexer.tokenize())