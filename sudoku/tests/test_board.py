"""
Various tests on the Sudoku board base class.

Tests in this module are using the board data `basic.clues`::

    ╔═══╤═══╤═══╦═══╤═══╤═══╦═══╤═══╤═══╗
    ║ 6 │ 8 │   ║ 4 │   │ 3 ║   │ 5 │   ║
    ╟───┼───┼───╫───┼───┼───╫───┼───┼───╢
    ║ 4 │   │ 2 ║   │ 5 │   ║ 3 │ 6 │ 8 ║
    ╟───┼───┼───╫───┼───┼───╫───┼───┼───╢
    ║ 5 │ 9 │ 3 ║ 6 │ 7 │ 8 ║   │   │ 4 ║
    ╠═══╪═══╪═══╬═══╪═══╪═══╬═══╪═══╪═══╣
    ║   │ 1 │ 7 ║ 2 │ 8 │ 6 ║ 9 │ 4 │ 5 ║
    ╟───┼───┼───╫───┼───┼───╫───┼───┼───╢
    ║ 8 │   │ 9 ║ 5 │   │ 4 ║ 2 │   │ 7 ║
    ╟───┼───┼───╫───┼───┼───╫───┼───┼───╢
    ║ 2 │ 5 │ 4 ║ 3 │ 9 │ 7 ║ 8 │ 1 │   ║
    ╠═══╪═══╪═══╬═══╪═══╪═══╬═══╪═══╪═══╣
    ║ 7 │   │   ║ 8 │ 3 │ 1 ║ 5 │ 9 │ 2 ║
    ╟───┼───┼───╫───┼───┼───╫───┼───┼───╢
    ║ 9 │ 3 │ 5 ║   │ 6 │   ║ 4 │   │ 1 ║
    ╟───┼───┼───╫───┼───┼───╫───┼───┼───╢
    ║   │ 2 │   ║ 9 │   │ 5 ║   │ 7 │ 3 ║
    ╚═══╧═══╧═══╩═══╧═══╧═══╩═══╧═══╧═══╝

"""
import re
from unittest import TestCase

from ..board import Board
from ..exceptions import InvalidBoard, InvalidMove

from .data import basic


class TestSetValue(TestCase):
    def setUp(self):
        self.board = Board(basic.clues)

    def test_bad_value(self):
        """
        A `ValueError` will be raised if the value to be set is too large.
        """
        message = re.escape("Value must be an integer between 1 and 9")
        with self.assertRaisesRegex(ValueError, message):
            self.board.set_value(0, 2, 10)

    def test_bad_move_box(self):
        message = re.escape("There is already a 4 in that box")
        with self.assertRaisesRegex(InvalidMove, message):
            self.board.set_value(4, 4, 4)

    def test_bad_move_column(self):
        message = re.escape("There is already a 7 in that column")
        with self.assertRaisesRegex(InvalidMove, message):
            self.board.set_value(0, 2, 7)

    def test_bad_move_row(self):
        message = re.escape("There is already a 7 in that row")
        with self.assertRaisesRegex(InvalidMove, message):
            self.board.set_value(2, 6, 7)

    def test_bad_move_everywhere(self):
        message = re.escape("There is already a 4 in that box and row and column")
        with self.assertRaisesRegex(InvalidMove, message):
            self.board.set_value(0, 6, 4)

    def test_good_move(self):
        row = 2
        column = 6
        value = 1

        # Before...
        box = self.board._get_box_index(row, column)
        self.assertEqual(self.board.get_value(row, column), 0)
        self.assertFalse(value in self.board._columns[column])
        self.assertFalse(value in self.board._rows[row])
        self.assertFalse(value in self.board._boxes[box])

        # Set value
        self.board.set_value(row, column, value)

        # After...
        self.assertEqual(self.board.get_value(row, column), value)
        self.assertTrue(value in self.board._columns[column])
        self.assertTrue(value in self.board._rows[row])
        self.assertTrue(value in self.board._boxes[box])


class TestGetBoxIndex(TestCase):
    def setUp(self):
        self.board = Board(basic.clues)

    def test_box_index(self):
        # First box
        index = self.board._get_box_index(0, 0)
        self.assertEqual(index, 0)
        index = self.board._get_box_index(2, 2)
        self.assertEqual(index, 0)

        # Second box
        index = self.board._get_box_index(2, 3)
        self.assertEqual(index, 1)
        index = self.board._get_box_index(1, 5)
        self.assertEqual(index, 1)

        # Third box
        index = self.board._get_box_index(0, 6)
        self.assertEqual(index, 2)
        index = self.board._get_box_index(2, 8)
        self.assertEqual(index, 2)

        # Seventh box
        index = self.board._get_box_index(6, 2)
        self.assertEqual(index, 6)
        index = self.board._get_box_index(8, 0)
        self.assertEqual(index, 6)

        # Ninth box
        index = self.board._get_box_index(6, 6)
        self.assertEqual(index, 8)
        index = self.board._get_box_index(8, 8)
        self.assertEqual(index, 8)

    def test_box_index_error(self):
        message = re.escape("Expecting an index from 0 to 8")
        with self.assertRaisesRegex(IndexError, message):
            self.board._get_box_index(6, 9)


class TestValidate(TestCase):
    """
    Check that invalid states are detected.

    Testing exception messages is a little tricky here, as the exception is
    thrown as soon as the first duplicate is detected.
    """
    def setUp(self):
        self.board = Board(basic.clues)

    def test_validate_good(self):
        self.board._validate()

    def test_validate_only_ones_error(self):
        """
        A board with the right length, but only ones.
        """
        self.board.data = [1] * 81
        message = re.escape("Duplicates found in box[0]: [1, 1, 1, 1, 1, 1, 1, 1, 1]")
        with self.assertRaisesRegex(InvalidBoard, message):
            self.board._validate()

    def test_validate_bad_box(self):
        self.board.data[2] = 8
        message = re.escape("Duplicates found in box[0]: [6, 8, 8, 4, 0, 2, 5, 9, 3]")
        with self.assertRaisesRegex(InvalidBoard, message):
            self.board._validate()

    def test_validate_bad_column(self):
        index = self.board._get_data_index(7, 3)
        self.board.data[index] = 4
        message = re.escape("Duplicates found in column[3]: [4, 0, 6, 2, 5, 3, 8, 4, 9]")
        with self.assertRaisesRegex(InvalidBoard, message):
            self.board._validate()

    def test_validate_bad_row(self):
        index = self.board._get_data_index(5, 7)
        self.board.data[index] = 3
        message = re.escape("Duplicates found in row[5]: [2, 5, 4, 3, 9, 7, 8, 3, 0]")
        with self.assertRaisesRegex(InvalidBoard, message):
            self.board._validate()


class TestGetValue(TestCase):
    @classmethod
    def setUpClass(cls):
        # Read-only tests: we can re-use board instance
        cls.board = Board(basic.clues)

    def test_get_value_bad_index(self):
        message = re.escape("Expecting an index from 0 to 8")
        with self.assertRaisesRegex(IndexError, message):
            self.board.get_value(0, 9)
        with self.assertRaisesRegex(IndexError, message):
            self.board.get_value(9, 0)

    def test_get_value(self):
        # First row
        self.assertEqual(self.board.get_value(0, 0), 6)
        self.assertEqual(self.board.get_value(0, 1), 8)
        self.assertEqual(self.board.get_value(0, 2), 0)
        self.assertEqual(self.board.get_value(0, 3), 4)

        self.assertEqual(self.board.get_value(0, 6), 0)
        self.assertEqual(self.board.get_value(0, 7), 5)
        self.assertEqual(self.board.get_value(0, 8), 0)

        # Fourth row
        self.assertEqual(self.board.get_value(3, 0), 0)
        self.assertEqual(self.board.get_value(3, 1), 1)
        self.assertEqual(self.board.get_value(3, 2), 7)

        # Ninth (and last) row
        self.assertEqual(self.board.get_value(8, 0), 0)
        self.assertEqual(self.board.get_value(8, 1), 2)
        self.assertEqual(self.board.get_value(8, 2), 0)

        self.assertEqual(self.board.get_value(8, 6), 0)
        self.assertEqual(self.board.get_value(8, 7), 7)
        self.assertEqual(self.board.get_value(8, 8), 3)


class TestGetBox(TestCase):
    @classmethod
    def setUpClass(cls):
        # Read-only tests: we can re-use board instance
        cls.board = Board(basic.clues)

    def test_get_box_first(self):
        first = self.board._get_box(0)
        self.assertEqual(first, [6, 8, 0, 4, 0, 2, 5, 9, 3])

    def test_get_box_last(self):
        first = self.board._get_box(8)
        self.assertEqual(first, [5, 9, 2, 4, 0, 1, 0, 7, 3])

    def test_get_box_all(self):
        """
        Box fetching is bloody fiddly work... Let's check 'em all.
        """
        expected_map = {
            0: [6, 8, 0, 4, 0, 2, 5, 9, 3],
            1: [4, 0, 3, 0, 5, 0, 6, 7, 8],
            2: [0, 5, 0, 3, 6, 8, 0, 0, 4],
            3: [0, 1, 7, 8, 0, 9, 2, 5, 4],
            4: [2, 8, 6, 5, 0, 4, 3, 9, 7],
            5: [9, 4, 5, 2, 0, 7, 8, 1, 0],
            6: [7, 0, 0, 9, 3, 5, 0, 2, 0],
            7: [8, 3, 1, 0, 6, 0, 9, 0, 5],
            8: [5, 9, 2, 4, 0, 1, 0, 7, 3],
        }
        for i in range(0, self.board.width):
            data = self.board._get_box(i)
            expected = expected_map[i]
            self.assertEqual(data, expected)

    def test_get_box_index_error(self):
        message = "Expecting an index from 0 to 8"
        with self.assertRaisesRegex(IndexError, message):
            self.board._get_box(9)


class TestGetColumn(TestCase):
    @classmethod
    def setUpClass(cls):
        # Read-only tests: we can re-use board instance
        cls.board = Board(basic.clues)

    def test_get_column_first(self):
        first = self.board._get_column(0)
        self.assertEqual(first, [6, 4, 5, 0, 8, 2, 7, 9, 0])

    def test_get_column_last(self):
        first = self.board._get_column(8)
        self.assertEqual(first, [0, 8, 4, 5, 7, 0, 2, 1, 3])

    def test_get_column_index_error(self):
        message = "Expecting an index from 0 to 8"
        with self.assertRaisesRegex(IndexError, message):
            self.board._get_column(9)


class TestGetRow(TestCase):
    @classmethod
    def setUpClass(cls):
        # Read-only tests: we can re-use board instance
        cls.board = Board(basic.clues)

    def test_get_row_first(self):
        first = self.board._get_row(0)
        self.assertEqual(first, [6, 8, 0, 4, 0, 3, 0, 5, 0])

    def test_get_row_last(self):
        last = self.board._get_row(8)
        self.assertEqual(last, [0, 2, 0, 9, 0, 5, 0, 7, 3])

    def test_get_row_index_error(self):
        message = "Expecting an index from 0 to 8"
        with self.assertRaisesRegex(IndexError, message):
            self.board._get_row(9)
