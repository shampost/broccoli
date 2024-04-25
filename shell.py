'''
SHELL
'''
from lexer import Lexer
from memory import Memory
from recursive_descent_parser import Parser

# global mem instance
memory = Memory()
parser = Parser(memory)

FILENAME = "test.txt"
with open(FILENAME, 'r', encoding='utf-8') as file:
    text = file.read()
lexer = Lexer(text)
tokenList = lexer.tokenize() # this call should not be needed?
#print(tokenList)
parser.set_tokens(tokenList)
parser.parse()
