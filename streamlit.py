import sys
from io import StringIO
from lexer import Lexer
from memory import Memory
from recursiveDescentParser import Parser
import streamlit as st

if "testKey" not in st.session_state:
    st.session_state["testKey"] = "testValue"
if "prevLines" not in st.session_state:
    st.session_state["prevLines"] = []

st.title("Broccoli")
# global mem instance
memory = Memory()
parser = Parser(memory)
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

def hitEnter(line: str):
    updateMemory()
    print(memory.getAll())
    parser = Parser(memory)
    lexer = Lexer(line)
    tokenList = lexer.tokenize()
    parser.setTokens(tokenList)
    parser.parse()
    st.header(parser.evaluate())
    updateSessionState()
    for line in st.session_state["prevLines"]:
        outputSlot.write(line)
    #st.write(st.session_state)

def updateSessionState():
    for key in memory.getAll().keys():
        st.session_state[key] = memory.getItem(key)
    lines = st.session_state["prevLines"]
    lines.append(line)
    st.session_state["prevLines"] = lines

def updateMemory():
    for key in st.session_state.keys():
        memory.addItem(name=key,value=st.session_state[key])

tab1, tab2 = st.tabs(["Terminal", "Upload File"])

with tab1:
    st.header("Terminal")
    outputSlot = st.container(height=400)
    inputSlot = st.empty()
    line = inputSlot.text_input(" ")
    if line:
        hitEnter(line)
   #st.button("Go", type="primary", on_click = hitEnter)
   

with tab2:
    st.header("Upload a file")
    #File upload stuff here
    filename = st.file_uploader("Upload a file", type="txt")
    onClick(filename)