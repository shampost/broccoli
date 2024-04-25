'''Lexer'''
from tokens import Token, TokenType
from errors import (
    InvalidCharacterException,
    NoValidTokenException,
    UnmatchedBracketException,
)
from memory import Memory
from errors import InvalidCharacterException, NoValidTokenException, UnmatchedParenthesesException


class Lexer:
    """
    # TODO: Write class docstring
    """

    def __init__(self, text: str):
        self.text = text
        self.pos = 0
        self.current_char = self.text[self.pos]
        self.line_tokens = []
        self.all_tokens = []
        self.line_count = 1
        self.paren_counter = 0
        self.curl_counter = 0

    def advance(self, by: int = 1):
        """
        # TODO: Write function docstring
        """
        self.pos += by
        if self.pos < len(self.text):
            self.current_char = self.text[self.pos]
        else:
            self.current_char = None

    def number(self):
        """
        DOCSTRING: The number() function is recursive and has 4 parts:
            1. While the current_char is a digit, it will be appended to 'result'
            2. If a decimal point is enountered, it is appended along with a recursive call to number()
            3. If the result contains a decimal point, the float number is returned
            4. Otherwise, it is either an integer, or the numbers past the decimal point in one of the recursions. Either way
                the int value can be returned.
        The else block contains error handling for the edge case of an input like "44.hi" which would raise a NoValidTokenError.
        All errors are caught and returned in the tokenize method.
        """
        result = ""
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
                raise NoValidTokenException(
                    f'\nNoValidTokenError on line {self.line_count}\n   Cannot create a token for "{result}"\n'
                )
        else:
            try:
                self.advance(by=-1)
                return int(result)
            except:
                raise NoValidTokenException(
                    f'\nNoValidTokenError: line {self.line_count}\n   Cannot create a token for "{self.text[self.pos-2:self.pos+1]}"\n'
                )

    def string(self):
        '''
        # TODO: write doctring
        '''
        result = ""
        while self.current_char is not None and self.current_char.isalpha():
            result += self.current_char
            self.advance()
        self.advance(by=-1)
        return result

    def get_next_token(self):
        '''
        # TODO: write doctring
        '''
        while self.current_char is not None:
            if self.current_char.isdigit():
                num = self.number()
                tokenType = TokenType.INT if type(num) == int else TokenType.FLOAT
                return Token(tokenType, num)
            elif self.current_char.isalpha():
                word = self.string()
                if word == "var":
                    return Token(TokenType.ID)
                elif word == "if":
                    return Token(TokenType.IF)
                elif word == "while":
                    return Token(TokenType.WHILE)
                elif word == "True":
                    return Token(TokenType.TRUE)
                elif word == "False":
                    return Token(TokenType.FALSE)
                else:
                    return Token(TokenType.STR, value=word)
            elif self.current_char == "+":
                return Token(TokenType.PLUS)
            elif self.current_char == "-":
                return Token(TokenType.MINUS)
            elif self.current_char == "*":
                return Token(TokenType.MULT)
            elif self.current_char == "/":
                return Token(TokenType.DIV)
            elif self.current_char == "=":
                return Token(TokenType.EQUALS)
            elif self.current_char == ":":
                return Token(TokenType.COLON)
            elif self.current_char == ",":
                return Token(TokenType.COMMA)
            elif self.current_char == "(":
                self.paren_counter += 1
                return Token(TokenType.LPAREN)
            elif self.current_char == ")":
                self.paren_counter -= 1
                return Token(TokenType.RPAREN)
            elif self.current_char == "{":
                self.curl_counter += 1
                return Token(TokenType.LCURL)
            elif self.current_char == "}":
                self.curl_counter -= 1
                return Token(TokenType.RCURL)
            elif self.current_char == "[":
                return Token(TokenType.LBRACKET)
            elif self.current_char == "]":
                return Token(TokenType.RBRACKET)
            elif self.current_char == '"':
                return Token(TokenType.QUOTE)
            elif self.current_char == "\n":
                return Token(TokenType.NEWLINE)
            elif self.current_char == "==":
                return Token(TokenType.TWOEQ)
            elif self.current_char == "<":
                return Token(TokenType.LESS)
            elif self.current_char == "<=":
                return Token(TokenType.LESSEQ)
            elif self.current_char == ">":
                return Token(TokenType.GREATER)
            elif self.current_char == ">=":
                return Token(TokenType.GREATEREQ)
            elif self.current_char == "|":
                return Token(TokenType.OR)
            elif self.current_char == "&":
                return Token(TokenType.AND)
            elif self.current_char == "!":
                return Token(TokenType.NOT)
            # Add new token conditions here after adding the new token to the tokens.py enum.
            raise InvalidCharacterException(
                f'\nInvalidCharacterError: line {self.line_count}\n   "{self.current_char}" is not part of the language\n'
            )

    def tokenize(self):
        '''
        # TODO: write doctring
        '''
        while self.current_char is not None:
            if self.current_char == " ":
                self.advance()
                continue
            if self.current_char == "\n":
                self.line_count += 1
                if len(self.line_tokens) != 0:
                    self.all_tokens.append(self.line_tokens)
                self.line_tokens = []
                self.advance()
                continue
            try:
                self.line_tokens.append(self.get_next_token())
                self.advance()
            except Exception as e:
                return e
        self.div_to_mult()
        if self.paren_counter != 0 or self.curl_counter != 0:
            raise UnmatchedBracketException(
                f"Missing parentheses on line {self.line_count}"
            )
        if len(self.line_tokens) != 0:
            self.all_tokens.append(self.line_tokens)
            self.line_tokens = []
        return self.all_tokens


    def div_to_mult(self):
        for i in range(len(self.line_tokens)):
            if self.line_tokens[i].type == TokenType.DIV:
                self.line_tokens[i].type = TokenType.MULT
                currentVal = self.line_tokens[i + 1].value
                newVal = 1 / int(currentVal)
                self.line_tokens[i + 1].type = TokenType.FLOAT
                self.line_tokens[i + 1].value = newVal
