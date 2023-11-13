from tokens import Token, TokenType

#########################################################
######################## LEXER ##########################
#########################################################
'''
TO USE:
    Create an instance of the Lexer by passing in a program as a string. Calling the tokenize() method on that instance 
    will return a list of tokens created from that text.

    If an invalid character is reached, tokenize() will instead return an error
'''
class InvalidCharacterError(Exception):
    pass

class Lexer:
    letters = ['a','b','c','d','e','f','g','h','i','j','k','l','m','n','o','p','q','r','s','t','u','v','w','x','y','z','A','B','C','D','E','F','G','H','I','J','K','L','M','N','O','P','Q','R','S','T','U','V','W','X','Y','Z']
    numbers = ['0','1','2','3','4','5','6','7','8','9']
        
    def __init__(self, text: str) -> None:
        self.text = text
        self.pos = 0
        self.tokens = []
        self.lineCount = 1
        self.word = ""
        self.number = ""
        self.prevLinesSum = 0

    def __repr__(self) -> str:
        return self.tokens
        
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
            self.prevLinesSum = self.pos
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
            raise InvalidCharacterError(f'\nInvalidCharacterError: line {self.lineCount}, position {self.pos-self.prevLinesSum + 1}\n   \"{current_char}\" is not part of the language\n')
        self.tokens.append(token) 
        self.pos += 1

    def tokenize(self) -> list[Token]:
        while self.pos < len(self.text):
            try:
                self.makeToken()
            except InvalidCharacterError as e:
                return e
        return self.tokens

lexer = Lexer("so, here is an& equation: (4*(5-2))")

print(lexer.tokenize())
