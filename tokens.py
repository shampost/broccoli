from enum import Enum

class TokenType(Enum):
    #TYPES
    INT     = object()
    FLOAT   = object()
    BOOL    = object()
    STR     = object()

    #
    RPAREN    = object()
    LPAREN    = object()
    RCURL     = object()
    LCURL     = object()
    RBRACKET  = object()
    LBRACKET  = object()
    QUOTE     = object()
    PLUS      = object()
    MINUS     = object()
    MULT      = object()
    DIV       = object()
    EQUALS    = object()
    COLON     = object()
    COMMA     = object()

    DOT       = object()

    NEWLINE   = object() 
    EOF       = object()

    ID        = object()

    LESS      = object()
    GREATER   = object()
    LESSEQ    = object()
    GREATEREQ = object()
    TWOEQ     = object()
    AND       = object()
    OR        = object()
    NOT       = object()

    WHILE     = object()
    IF        = object()

    TRUE      = object()
    FALSE     = object()




class Token:
    def __init__(self, type: TokenType, value=None) -> None:
        self.type = type
        self.value = value
    
    def __repr__(self) -> str:
        if self.value: 
            return f'({self.type} : {self.value})'
        return f'({self.type})'
