from lexer import Lexer
from stem import Parser
while True:
    text = input("broccoli > ")
    lexer = Lexer(text)
    tokens = lexer.tokenize()
    parser = Parser(tokens)
    ast = parser.parse()
    print(ast)