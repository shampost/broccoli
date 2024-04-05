import sys
from io import StringIO
from lexer import Lexer
from memory import Memory
from recursiveDescentParser import Parser

# global mem instance
memory = Memory()
parser = Parser(memory)

filename = "test.txt"
with open(filename, 'r') as file:
    text = file.read()
lexer = Lexer(text)
tokenList = lexer.tokenize() # this call should not be needed?
#print(tokenList)
parser.setTokens(tokenList)
parser.parse()
print(f'>> {parser.evaluate()}')