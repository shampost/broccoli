TT_INT =    "TT_INT"
TT_STR =    "STR"
TT_BOOL =   "BOOL"
TT_FLOAT =  "FLOAT"

TT_OPER =   "OPER"

TT_RPAREN = "RPAREN"
TT_LPAREN = "LPAREN"

class Token():
    def __init__(self, type: str, value = None):
        self.type = type
        self.value = value
    
    def __repr__(self) -> str:

        if self.value: return f'{self.type} : {self.value}'
        return f'{self.type}'

minusToken = Token(TT_OPER, "-")
plusToken = Token(TT_OPER, "+")

