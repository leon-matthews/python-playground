
from pprint import pprint as pp
from unittest import skip, TestCase

from ..lempel_ziv import look_back, Token, tokenise, untokenise


# ~ def load_tests(loader, tests, ignore):
    # ~ tests.addTests(doctest.DocTestSuite(lempel_ziv))
    # ~ return tests


class LookBackTest(TestCase):
    def test_empty(self) -> None:
        self.assertIsNone(look_back('', ''))

    @skip('todo')
    def test_easy(self) -> None:
        index = look_back('t', 'Hamlet')
        self.assertEqual(index, 1)


class TokenTest(TestCase):
    def test_repr(self) -> None:
        self.assertEqual(repr(Token(1, 2)), "Token(1, 2)")
        self.assertEqual(repr(Token(1, 2, 'A')), "Token(1, 2, 'A')")

    def test_str(self) -> None:
        self.assertEqual(str(Token(1, 2)), "(1, 2)")
        self.assertEqual(str(Token(1, 2, 'A')), "(1, 2, 'A')")


class TokeniseTest(TestCase):
    def test_empty(self) -> None:
        tokens = tokenise('')
        self.assertEqual(tokens, [])

    @skip('todo')
    def test_single_character(self) -> None:
        string = 't'
        tokens = tokenise(string)
        self.assertEqual(tokens, [Token(0, 1, 't')])

    @skip('todo')
    def test_soliloquy(self) -> None:
        string = 'to be or not to be'
        tokens = tokenise(string)
        pp(tokens)


class UntokeniseTest(TestCase):
    def test_empty(self) -> None:
        tokens: list[Token] = []
        string = untokenise(tokens)
        self.assertEqual(string, '')

    def test_single_character(self) -> None:
        tokens = [Token(0, 1, 't')]
        string = untokenise(tokens)
        self.assertEqual(string, 't')
