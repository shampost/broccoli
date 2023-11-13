from lexer import Lexer

while True:
    text = input("broccoli > ")
    lexer = Lexer(text)
    print(lexer.tokenize())