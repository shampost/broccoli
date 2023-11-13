class Token:
    def __init__(self, type, value=None):
        self.type = type
        self.value = value

    def __repr__(self):
        return 'Token({type}, {value})'.format(
            type=self.type,
            value=repr(self.value)
        )

class Lexer:
    def __init__(self, text):
        self.text = text
        self.pos = 0
        self.current_char = self.text[self.pos]
        self.tokens = []

    def error(self):
        raise Exception('Invalid character')

    def advance(self):
        self.pos += 1
        if self.pos < len(self.text):
            self.current_char = self.text[self.pos]
        else:
            self.current_char = None

    def integer(self):
        result = ''
        while self.current_char is not None and self.current_char.isdigit():
            result += self.current_char
            self.advance()
        return int(result)

    #def string(self):
        #result = ''
        #while self.current_char is not None and self.current_char.ischar():
            #result += self.current_char
            #self.advance()
        #return result

    def get_next_token(self):
        while self.current_char is not None:
            if self.current_char.isspace():
                self.advance()
                continue
            if self.current_char.isdigit():
                return Token('INTEGER', self.integer())
            if self.current_char == '+':
                self.advance()
                return Token('PLUS', '+')
            if self.current_char == '-':
                self.advance()
                return Token('MINUS', '-')
            if self.current_char == '*':
                self.advance()
                return Token('MULTIPLY', '*')
            if self.current_char == '/':
                self.advance()
                return Token('DIVIDE', '/')
            self.error()
        return Token('EOF', None)
    
    def tokenize(self):
        while self.pos < len(self.text):
            self.tokens.append(self.get_next_token())
        return self.tokens