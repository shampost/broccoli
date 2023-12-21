from lexer import Lexer
from recursiveDescentParser import Parser

parser = Parser()
while True:
    text = input("broccoli > ")
    if text == "":
        continue
    lexer = Lexer(text)
    tokenList = lexer.tokenize()
    print(tokenList)
    parser.setTokens(tokenList=tokenList)
    parser.parse()
    print(parser.evaluate())