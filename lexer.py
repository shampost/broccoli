from tokens import Token, TokenType
from errors import InvalidCharacterException, NoValidTokenException, UnmatchedParenthesesException


class Lexer:
    def __init__(self, text: str):
        self.text = text
        self.pos = 0
        self.current_char = self.text[self.pos]
        self.lineTokens = []
        self.allTokens = []
        self.lineCount = 1
        self.parenCounter = 0

    def advance(self, by: int = 1):
        self.pos += by
        if self.pos < len(self.text):
            self.current_char = self.text[self.pos]
        else:
            self.current_char = None

    '''
    DOCSTRING: The number() function is recursive and has 4 parts:
        1. While the current_char is a digit, it will be appended to 'result'
        2. If a decimal point is enountered, it is appended along with a recursive call to number()
        3. If the result contains a decimal point, the float number is returned
        4. Otherwise, it is either an integer, or the numbers past the decimal point in one of the recursions. Either way
            the int value can be returned.
    The else block contains error handling for the edge case of an input like "44.hi" which would raise a NoValidTokenError.
    All errors are caught and returned in the tokenize method.
    '''
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
            try:
                return float(result)
            except:
                raise NoValidTokenException(f'\nNoValidTokenError on line {self.lineCount}\n   Cannot create a token for \"{result}\"\n')
        else:
            try:
                self.advance(by=-1)
                return int(result)
            except:
                raise NoValidTokenException(f'\nNoValidTokenError: line {self.lineCount}\n   Cannot create a token for \"{self.text[self.pos-2:self.pos+1]}\"\n')

    def string(self):
        result = ''
        while self.current_char is not None and self.current_char.isalpha():
            result += self.current_char
            self.advance()
        self.advance(by=-1)
        return result

    def get_next_token(self):
        while self.current_char is not None:
            if self.current_char.isdigit():
                num = self.number()
                tokenType = TokenType.INT if type(num) == int else TokenType.FLOAT
                return Token(tokenType, num)
            elif self.current_char.isalpha():
                word = self.string()
                if word == "var":
                    return Token(TokenType.ID)
                else:
                    return Token(TokenType.STR, value=word)
            elif self.current_char == '+':
                return Token(TokenType.PLUS) 
            elif self.current_char == '-':
                return Token(TokenType.MINUS) 
            elif self.current_char == '*':
                return Token(TokenType.MULT) 
            elif self.current_char == '/':
                return Token(TokenType.DIV) 
            elif self.current_char == "=":
                return Token(TokenType.EQUALS)
            elif self.current_char == ":":
                return Token(TokenType.COLON)
            elif self.current_char == ",":
                return Token(TokenType.COMMA)
            elif self.current_char == "(":
                self.parenCounter += 1
                return Token(TokenType.LPAREN) 
            elif self.current_char == ")":
                self.parenCounter -= 1 
                return Token(TokenType.RPAREN)
            elif self.current_char == "{":
                return Token(TokenType.LCURL)
            elif self.current_char == "}":
                return Token(TokenType.RCURL)
            elif self.current_char == "[":
                return Token(TokenType.LBRACKET)
            elif self.current_char == "]":
                return Token(TokenType.RBRACKET)
            elif self.current_char == "\"":
                return Token(TokenType.QUOTE)
            elif self.current_char == "\n":
                return Token(TokenType.NEWLINE)
            #Add new token conditions here after adding the new token to the tokens.py enum.
            raise InvalidCharacterException(f'\nInvalidCharacterError: line {self.lineCount}\n   \"{self.current_char}\" is not part of the language\n')
    
    def tokenize(self):
        while self.current_char is not None:
            if self.current_char == " ":
                self.advance()
                continue
            elif self.current_char == '\n':
                self.lineCount += 1
                self.allTokens.append(self.lineTokens)
                self.lineTokens = []
                self.advance()
                continue
            try:
                self.lineTokens.append(self.get_next_token())
                self.advance()
            except Exception as e: 
                return e
        self.divToMult()
        if self.parenCounter != 0:
            raise UnmatchedParenthesesException(f'Missing parentheses on line {self.lineCount}')
        if len(self.lineTokens) != 0:
            self.allTokens.append(self.lineTokens)
            self.lineTokens = []
        return self.allTokens

    def divToMult(self):
        for i in range(len(self.lineTokens)):
            if self.lineTokens[i].type == TokenType.DIV:
                self.lineTokens[i].type = TokenType.MULT
                currentVal = self.lineTokens[i+1].value
                newVal = 1/currentVal
                self.lineTokens[i+1].type = TokenType.FLOAT
                self.lineTokens[i+1].value = newVal