
from unittest import skip, TestCase

from sudoku import board, utils

from .data import basic, strings


class ImportTestCase(TestCase):
    def _check_numbers(self, numbers):
        # General properties
        self.assertEqual(len(numbers), 81)
        for n in numbers:
            self.assertIsInstance(n, int)
            self.assertLess(n, 10)

        # Exact match
        self.assertEqual(numbers, basic.clues)


class TestImportString(ImportTestCase):
    """
    We can import various text formats.
    """

    def test_import_expected(self):
        """
        Ordinary string, one number per character.
        """
        numbers = utils.import_string(basic.clues_string)
        self._check_numbers(numbers)

    def test_import_alternative(self):
        """
        As per `test_expected`, but a full-stop is used in place of zero.
        """
        numbers = utils.import_string(basic.clues_full_stops)
        self._check_numbers(numbers)

    def test_import_ascii_grid(self):
        """
        Attempt to import grid exported by `render.draw_ascii()`.
        """
        numbers = utils.import_string(strings.ascii_grid)
        self._check_numbers(numbers)


class TestImportUnicode(ImportTestCase):
    def test_import_unicode_grid(self):
        """
        Attempt to import grid exported by `render.draw_ascii()`.
        """
        numbers = utils.import_unicode(strings.unicode_grid)
        self._check_numbers(numbers)
