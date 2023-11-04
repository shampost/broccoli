from tokens import Token, TokenType

class Lexer:
    def __init__(self, text: str) -> None:
        self.text = text
        self.pos = 0
        self.tokens = []
        self.lineCount = 1
        self.letters = ['a','b','c','d','e','f','g','h','i','j','k','l','m','n','o','p','q','r','s','t','u','v','w','x','y','z','A','B','C','D','E','F','G','H','I','J','K','L','M','N','O','P','Q','R','S','T','U','V','W','X','Y','Z']
        self.numbers = ['0','1','2','3','4','5','6','7','8','9']
        self.word = ""
        self.number = ""

    def __repr__(self) -> str:
        return self.tokens

    def makeNumber(self):
        while self.text[self.pos] in self.numbers:
            self.number += self.text[self.pos]
            self.pos += 1
        token = Token(TokenType.INT, self.number)
        self.number = ""
        return token
    def makeWord(self):
        while self.text[self.pos] in self.letters:
            self.word += self.text[self.pos]
            self.pos += 1
        token = Token(TokenType.STR, self.word)
        self.word = ""
        return token

    def advance(self):
        self.pos += 1
        
    def makeToken(self):
        token = None
        current_char = self.text[self.pos]

        while current_char in self.numbers:
            self.number += current_char
            self.pos += 1
            if self.pos < len(self.text): 
                current_char = self.text[self.pos]
            else: 
                break
        if self.number != "":
            self.tokens.append(Token(TokenType.INT, self.number))
            self.number = ""
            return
        while current_char in self.letters:
            self.word += current_char
            self.pos += 1
            if self.pos < len(self.text): 
                current_char = self.text[self.pos]
            else: 
                break
        if self.word != "":
            self.tokens.append(Token(TokenType.STR, self.word))
            self.word = ""
            return


        if current_char == " ":
            self.pos += 1
            return
        elif current_char == "\n":
            self.lineCount += 1
            self.pos += 1
            return
        elif current_char == "+":
            token = Token(TokenType.PLUS) 
        elif current_char == "-":
            token = Token(TokenType.MINUS) 
        elif current_char == "*":
            token = Token(TokenType.MULT)
        elif current_char == "/":
            token = Token(TokenType.DIV)
        elif current_char == "=":
            token = Token(TokenType.EQUALS)
        elif current_char == ":":
            token = Token(TokenType.COLON)
        elif current_char == ",":
            token = Token(TokenType.COMMA)
        elif current_char == "(":
            token = Token(TokenType.LPAREN) 
        elif current_char == ")":
            token = Token(TokenType.RPAREN)
        elif current_char == "{":
            token = Token(TokenType.LCURL)
        elif current_char == "}":
            token = Token(TokenType.RCURL)
        elif current_char == "[":
            token = Token(TokenType.LBRACKET)
        elif current_char == "]":
            token = Token(TokenType.RBRACKET)
        elif current_char == "\"":
            token = Token(TokenType.QUOTE)
        

        if token == None:
            raise SyntaxError(f'Invalid character \"{current_char}\" on line {self.lineCount} position {self.pos+1}')
        self.tokens.append(token) 
        self.pos += 1

    def tokenize(self) -> list[Token]:
        while self.pos < len(self.text):
            self.makeToken()
        return self.tokens

lexer = Lexer("so, here is an equation: (4*(5-2))")

print(lexer.tokenize())