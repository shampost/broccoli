import sys
from io import StringIO
from lexer import Lexer
from memory import Memory
from recursiveDescentParser import Parser
import streamlit as st

st.title("Broccoli")
# global mem instance
memory = Memory()
parser = Parser(memory)
#while True:
#    text = input("broccoli > ")
#    if text == "":
#        continue
# filename = "test.txt"
def onClick(filename):
    if filename is None:
        return
    # using streamlit and StringIO to read file
    stringIO = StringIO(filename.getvalue().decode('utf-8'))
    text = stringIO.read()
    lexer = Lexer(text)
    tokenList = lexer.tokenize() # this call should not be needed?
    print(tokenList)
    parser.setTokens(tokenList)
    parser.parse()
    st.header(parser.evaluate())

filename = st.file_uploader("Upload a file", type="txt")

onClick(filename)
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