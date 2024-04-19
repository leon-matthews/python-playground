
from unittest import TestCase

from sudoku.board import Board
from sudoku.render import draw_ascii, draw_unicode

from .data import basic
from .data.strings import ascii_grid, unicode_grid


class TestRender(TestCase):
    def test_ascii(self):
        b = Board(basic.clues)
        text = draw_ascii(b)
        self.assertEqual(text, ascii_grid)

    def test_unicode(self):
        b = Board(basic.clues)
        text = draw_unicode(b)
        self.assertEqual(text, unicode_grid)
