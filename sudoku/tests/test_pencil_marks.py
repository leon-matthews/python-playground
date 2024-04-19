
from unittest import skip, TestCase

from sudoku.board import Board, PencilMarked
from sudoku import exceptions

from .data import basic


@skip("Refactoring")
class TestPencilMarkedCandidates(TestCase):
    @classmethod
    def setUpClass(cls):
        cls.board = PencilMarked(basic.clues)

    def test_possibility_solved(self):
        candidates = self.board.candidates(0, 0)
        self.assertEqual(candidates, [])

        candidates = self.board.candidates(8, 8)
        self.assertEqual(candidates, [])

    def test_single_possibility(self):
        candidates = self.board.candidates(2, 0)
        self.assertEqual(candidates, [1])

        candidates = self.board.candidates(1, 1)
        self.assertEqual(candidates, [7])

    def test_possibilities(self):
        candidates = self.board.candidates(2, 8)
        self.assertEqual(candidates, [1, 6, 8])


@skip("Refactoring")
class TestPencilMarkedRebuild(TestCase):
    @classmethod
    def setUpClass(cls):
        cls.board = PencilMarked(basic.clues)

    def test_empty_clues(self):
        message = r"Expecting 81 numbers, 0 given"
        with self.assertRaisesRegex(exceptions.SudokuError, message):
            clues = []
            Board(clues)

    def test_build_rows(self):
        expected_rows = {
            0: {3, 4, 5, 6, 8},
            1: {2, 3, 4, 5, 6, 8},
            2: {3, 4, 5, 6, 7, 8, 9},
            3: {1, 2, 4, 5, 6, 7, 8, 9},
            4: {2, 4, 5, 7, 8, 9},
            5: {1, 2, 3, 4, 5, 7, 8, 9},
            6: {1, 2, 3, 5, 7, 8, 9},
            7: {1, 3, 4, 5, 6, 9},
            8: {2, 3, 5, 7, 9}
        }
        self.assertEqual(self.board.rows, expected_rows)

    def test_build_columns(self):
        expected_columns = {
            0: {2, 4, 5, 6, 7, 8, 9},
            1: {1, 2, 3, 5, 8, 9},
            2: {2, 3, 4, 5, 7, 9},
            3: {2, 3, 4, 5, 6, 8, 9},
            4: {3, 5, 6, 7, 8, 9},
            5: {1, 3, 4, 5, 6, 7, 8},
            6: {2, 3, 4, 5, 8, 9},
            7: {1, 4, 5, 6, 7, 9},
            8: {1, 2, 3, 4, 5, 7, 8}
        }
        self.assertEqual(self.board.columns, expected_columns)

    def test_build_boxes(self):
        expected_boxes = {
            0: {2, 3, 4, 5, 6, 8, 9},
            1: {3, 4, 5, 6, 7, 8},
            2: {3, 4, 5, 6, 8},
            3: {1, 2, 4, 5, 7, 8, 9},
            4: {2, 3, 4, 5, 6, 7, 8, 9},
            5: {1, 2, 4, 5, 7, 8, 9},
            6: {2, 3, 5, 7, 9},
            7: {1, 3, 5, 6, 8, 9},
            8: {1, 2, 3, 4, 5, 7, 9}
        }
        self.assertEqual(self.board.boxes, expected_boxes)
