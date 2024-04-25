import unittest
from lexer import Lexer, NoValidTokenException

class TestLexer(unittest.TestCase):
    def test_number(self):
        # Test integer number
        lexer = Lexer("123")
        self.assertEqual(lexer.number(), 123)

        # Test float number
        lexer = Lexer("123.456")
        self.assertEqual(lexer.number(), 123.456)

        # Test invalid number
        lexer = Lexer("123.456.789")
        with self.assertRaises(NoValidTokenException):
            lexer.number()

if __name__ == "__main__":
    unittest.main()