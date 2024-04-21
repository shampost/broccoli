'''Module providing exceptions'''

class InvalidCharacterException(Exception):
    '''
    # TODO: write docstring
    '''
    #Raised when that character does not exist in the grammar.

class NoValidTokenException(Exception):
    '''
    # TODO: write docstring
    '''
    #Raised when a combination of valid characters does not make up a valid token.

class UnmatchedBracketException(Exception):
    '''
    # TODO: write docstring
    '''
    #Raised when a combination of valid characters does not make up a valid token.

class InvalidRedeclaration(Exception):
    '''
    # TODO: write docstring
    '''
    #Raised when a variable has already been declared and is being redeclared within local scope
