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
parser.setTokens(tokenList)
parser.parse()
print(parser.evaluate())

# def main():
#     parser = Parser()
#     filename = sys.argv[1]
#     with open(filename, 'r') as file:
#         text = file.read()
#     lexer = Lexer(text)
#     tokenList = lexer.tokenize()
#     parser.setTokens(tokenList)
#     print(lexer.lineTokens)
#     parser.parse()
#     print(parser.evaluate())

# if __name__ == '__main__':
#     main()