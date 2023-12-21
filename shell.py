from lexer import Lexer

while True:
    text = input("broccoli > ")
    if text == "":
        continue
    lexer = Lexer(text)
    tokenList = lexer.tokenize()
    parser.setTokens(tokenList=tokenList)
    parser.parse()
    print(parser.evaluate())