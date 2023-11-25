from lexer import Lexer
from recursiveDescentParser import Parser

while True:
    text = input("broccoli > ")
    lexer = Lexer(text)
    tokenList = lexer.tokenize()
    parser = Parser(tokenList)
    parser.parse()
    print(parser.evaluate())