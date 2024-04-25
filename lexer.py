"""
This module contains the Lexer class, which is used to convert a string of text\
    into a list of tokens.

The Lexer class takes a string of text as input and processes it one character at\
    a time. It recognizes tokens that represent integers, floats, identifiers, keywords,\
    and various operators. The recognized tokens are stored in a list.

The Lexer class also keeps track of the current position in the text,\
    the current character being processed, and the line number. It has\
    methods to advance the current position and to recognize individual tokens.

The Lexer class uses the Token and TokenType classes from the\
    tokens module to represent the recognized tokens. It raises\
    exceptions defined in the errors module when it encounters invalid characters or tokens.

This module is part of a simple interpreter for a programming language.
"""

from tokens import Token, TokenType
from errors import (
    InvalidCharacterException,
    NoValidTokenException,
    UnmatchedBracketException,
)

class Lexer:
    """
    The Lexer class converts a string of text into a list of tokens.

    Methods:
    1. __init__: Initializes the Lexer with the input text and sets the initial position to 0.
    2. advance: Advances the current position by a specified number of characters.
    3. number: Recognizes and returns a number token (integer or float).
    4. string: Recognizes and returns a string token (identifier or keyword).
    5. get_next_token: Recognizes and returns the next token.
    6. tokenize: Processes the input text character by character to tokenize the text.
    7. divToMult: Converts division tokens to multiplication tokens.
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
        '''
        Advances the current position by a specified number of characters.

        PARAMETERS:
            by (int): The number of characters to advance the current position by.

        RETURNS:
            None
        '''
        self.pos += by
        if self.pos < len(self.text):
            self.current_char = self.text[self.pos]
        else:
            self.current_char = None

    def number(self):
        '''
        The number() function is recursive and operates in four parts:

        1. Appends each digit to 'result' while the current character is a digit.
        2. If a decimal point is encountered, it is appended and number() is called recursively.
        3. If 'result' contains a decimal point, a float is returned.
        4. Otherwise, an integer is returned. This includes numbers past the decimal point in recursive calls.

        The function handles edge cases like "44.hi" which would raise a NoValidTokenError. All errors are caught and returned in the tokenize method.

        Parameters:
            None

        Returns:
            The recognized integer or float number token from the input text.
        '''
        result = ""
        while self.current_char is not None and self.current_char.isdigit():
            result += self.current_char
            self.advance()
        if self.current_char == ".":
            result += "."
            self.advance()
            while self.current_char is not None and self.current_char.isdigit():
                result += self.current_char
                self.advance()
        try:
            return int(result) if '.' not in result else float(result)
        except ValueError:
            raise NoValidTokenException(f"Invalid number: {result}") # syntax error raised before this exception

        # result = ""
        # while self.current_char is not None and self.current_char.isdigit():
        #     result += self.current_char
        #     self.advance()
        # if self.current_char == ".":
        #     result += "."
        #     self.advance()
        #     result += str(self.number())
        # if "." in result:
        #     try:
        #         return float(result)
        #     except Exception as exc:
        #         raise NoValidTokenException(
        #             f"\nNoValidTokenError on line {self.line_count}\n   Cannot create a"
        #             f' token for "{result}"\n'
        #         ) from exc
        # else:
        #     try:
        #         self.advance(by=-1)
        #         return int(result)
        #     except Exception as exc:
        #         raise NoValidTokenException(
        #             f"\nNoValidTokenError: line {self.line_count}\n   Cannot create a"
        #             f' token for "{self.text[self.pos-2:self.pos+1]}"\n'
        #         ) from exc

    def string(self):
        ''' 
        Recognizes and returns a string token from the input text.

        This method identifies identifiers and keywords in the input text. It 
        continues to append characters to the token as long as the current 
        character is alphabetic.

        Parameters: 
            None

        Returns: 
            A string token from the input text.
        '''
        result = ""
        while self.current_char is not None and self.current_char.isalpha():
            result += self.current_char
            self.advance()
        self.advance(by=-1)
        return result

    def get_next_token(self):
        '''
        Identifies and returns the next token from the input text.

        This method scans the input text and identifies the next valid token. 
        It can recognize different types of tokens such as integers, floats, 
        identifiers, keywords, and operators.

        Parameters: 
            None

        Returns:
            The next token from the input text.
        '''
        while self.current_char is not None:
            if self.current_char.isdigit():
                num = self.number()
                token_type = TokenType.INT if type(num) == int else TokenType.FLOAT
                return Token(token_type, num)
            if self.current_char.isalpha():
                word = self.string()
                if word == "var":
                    return Token(TokenType.ID)
                if word == "if":
                    return Token(TokenType.IF)
                if word == "while":
                    return Token(TokenType.WHILE)
                if word == "True":
                    return Token(TokenType.TRUE)
                if word == "False":
                    return Token(TokenType.FALSE)
                if word == "print":
                    return Token(TokenType.PRINT)
                return Token(TokenType.STR, value=word)
            if self.current_char == "+":
                return Token(TokenType.PLUS)
            if self.current_char == "-":
                return Token(TokenType.MINUS)
            if self.current_char == "*":
                return Token(TokenType.MULT)
            if self.current_char == "/":
                return Token(TokenType.DIV)
            if self.current_char == "=":
                return Token(TokenType.EQUALS)
            if self.current_char == ":":
                return Token(TokenType.COLON)
            if self.current_char == ",":
                return Token(TokenType.COMMA)
            if self.current_char == "(":
                self.paren_counter += 1
                return Token(TokenType.LPAREN)
            if self.current_char == ")":
                self.paren_counter -= 1
                return Token(TokenType.RPAREN)
            if self.current_char == "{":
                self.curl_counter += 1
                return Token(TokenType.LCURL)
            if self.current_char == "}":
                self.curl_counter -= 1
                return Token(TokenType.RCURL)
            if self.current_char == "[":
                return Token(TokenType.LBRACKET)
            if self.current_char == "]":
                return Token(TokenType.RBRACKET)
            if self.current_char == '"':
                return Token(TokenType.QUOTE)
            if self.current_char == "\n":
                return Token(TokenType.NEWLINE)
            if self.current_char == "==":
                return Token(TokenType.TWOEQ)
            if self.current_char == "<":
                return Token(TokenType.LESS)
            if self.current_char == "<=":
                return Token(TokenType.LESSEQ)
            if self.current_char == ">":
                return Token(TokenType.GREATER)
            if self.current_char == ">=":
                return Token(TokenType.GREATEREQ)
            if self.current_char == "|":
                return Token(TokenType.OR)
            if self.current_char == "&":
                return Token(TokenType.AND)
            if self.current_char == "!":
                return Token(TokenType.NOT)
            # Add new token conditions here after adding the new token to the tokens.py enum.
            raise InvalidCharacterException(
                f"\nInvalidCharacterError: line {self.line_count}\n  "
                f' "{self.current_char}" is not part of the language\n'
            )

    def tokenize(self):
        '''
        Processes the input text character by character to recognize and tokenize the text.

        This method iterates over the input text and uses the get_next_token method to recognize tokens.
        Whitespace characters are skipped, and newline characters increment the line count and reset the line tokens.
        If an InvalidCharacterException is raised, it is returned and the tokenization process stops.
        After all characters have been processed, the divToMult method is called to convert division tokens to multiplication tokens.
        If there are unmatched parentheses or curly braces, an UnmatchedBracketException is raised.

        Parameters: 
            None

        Returns:
            A list of all recognized tokens. If an InvalidCharacterException is raised during tokenization, the exception is returned instead.
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
            except InvalidCharacterException as e:
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
        '''
        Converts division tokens to multiplication tokens in the token list.
        
        Parameters:
            None
        
        Returns:
            None
        '''
        for i, token in enumerate(self.line_tokens):
            if token.type == TokenType.DIV:
                token.type = TokenType.MULT
                next_token = self.line_tokens[i + 1]
                next_token.value = 1 / next_token.value
                next_token.type = TokenType.FLOAT
