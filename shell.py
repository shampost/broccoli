import sys
from lexer import Lexer
from recursiveDescentParser import Parser

parser = Parser()
#while True:
#    text = input("broccoli > ")
#    if text == "":
#        continue
filename = "test.txt"
with open(filename, 'r') as file:
    text = file.read()
lexer = Lexer(text)
tokenList = lexer.tokenize()
parser.setTokens(tokenList=tokenList)
parser.parse()
print(parser.evaluate())