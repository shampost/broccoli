from lexer import Lexer
from recursiveDescentParser import Parser

parser = Parser()
while True:
    text = input("broccoli > ")
    lexer = Lexer(text)
    tokenList = lexer.tokenize()
    parser.setTokens(tokenList=tokenList)
    #print(tokenList)
    parser.parse()
    print(parser.evaluate())