from tokens import Token, TokenType
from errors import InvalidCharacterError, InvalidInputError


class Lexer:
    def __init__(self, text: str):
        self.text = text
        self.pos = 0
        self.current_char = self.text[self.pos]
        self.tokens = []
        self.lineCount = 0

    def advance(self):
        self.pos += 1
        if self.pos < len(self.text):
            self.current_char = self.text[self.pos]
        else:
            self.current_char = None

    def number(self):
        result = ''
        while self.current_char is not None and self.current_char.isdigit():
            result += self.current_char
            self.advance()
        if self.current_char == ".": 
            result += "."
            self.advance()
            result += str(self.number())
        if "." in result:
            return float(result)
        else:
            try:
                return int(result)
            except:
                raise InvalidInputError(f'\nInvalidInputError: line {self.lineCount}, position {self.pos}\n   No valid token for \"{self.text[self.pos-2:self.pos+1]}\"\n')

    def string(self):
        result = ''
        while self.current_char is not None and self.current_char.isalpha():
            result += self.current_char
            self.advance()
        return result

    def get_next_token(self):
        if self.current_char.isdigit():
            num = self.number()
            tokenType = TokenType.INT if type(num) == int else TokenType.FLOAT
            return Token(tokenType, num)
        if self.current_char.isalpha():
            return Token(TokenType.STR, self.string())
        if self.current_char == '+':
            self.advance()
            return Token(TokenType.PLUS) 
        if self.current_char == '-':
            self.advance()
            return Token(TokenType.MINUS) 
        if self.current_char == '*':
            self.advance()
            return Token(TokenType.MULT) 
        if self.current_char == '/':
            self.advance()
            return Token(TokenType.DIV) 
        elif self.current_char == "=":
            self.advance()
            return Token(TokenType.EQUALS)
        elif self.current_char == ":":
            self.advance()
            return Token(TokenType.COLON)
        elif self.current_char == ",":
            self.advance()
            return Token(TokenType.COMMA)
        elif self.current_char == "(":
            self.advance()
            return Token(TokenType.LPAREN) 
        elif self.current_char == ")":
            self.advance()
            return Token(TokenType.RPAREN)
        elif self.current_char == "{":
            self.advance()
            return Token(TokenType.LCURL)
        elif self.current_char == "}":
            self.advance()
            return Token(TokenType.RCURL)
        elif self.current_char == "[":
            self.advance()
            return Token(TokenType.LBRACKET)
        elif self.current_char == "]":
            self.advance()
            return Token(TokenType.RBRACKET)
        elif self.current_char == "\"":
            self.advance()
            return Token(TokenType.QUOTE)
        raise InvalidCharacterError(f'\nInvalidCharacterError: line {self.lineCount}, position {self.pos}\n   \"{self.current_char}\" is not part of the language\n')
    
    def tokenize(self):
        while self.pos < len(self.text):
            if self.current_char.isspace():
                self.advance()
                continue
            elif self.current_char == "\n": #This doesnt work
                self.lineCount += 1
                self.advance()
                print(self.lineCount)
                continue
            try:
                self.tokens.append(self.get_next_token())
            except Exception as e:
                return e
        return self.tokens