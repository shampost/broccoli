"""This module contains custom exceptions for the compiler."""
class InvalidCharacterException(Exception):
    """Raised when that character does not exist in the grammar."""

class NoValidTokenException(Exception):
    """Raised when a combination of valid characters does not make up a valid token."""

class UnmatchedBracketException(Exception):
    """Raised when a combination of valid characters does not make up a valid token."""

class InvalidRedeclaration(Exception):
    """Raised when a variable has already been declared and is being\
         redeclared within local scope."""
