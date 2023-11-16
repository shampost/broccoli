class InvalidCharacterException(Exception):
    #Raised when that character does not exist in the grammar.
    pass

class NoValidTokenException(Exception):
    #Raised when a combination of valid characters does not make up a valid token.
    pass