
from unittest import skip, TestCase

from sudoku.board import PencilMarked
from sudoku import examples
from sudoku.solvers import single_candidates, single_candidates_all
from sudoku import utils

from .data import basic


@skip("Refactoring")
class TestSingleCandidates(TestCase):
    def test_single_candidates(self):
        puzzle = PencilMarked(basic.clues)
        num_solved = single_candidates(puzzle)
        self.assertEqual(num_solved, 19)
        self.assertEqual(puzzle.unsolved(), 4)

    def test_single_candidates_all(self):
        clues = utils.import_string(examples.beginner_6)
        puzzle = PencilMarked(clues)
        num_solved = single_candidates_all(puzzle)
        self.assertEqual(puzzle.is_solved(), True)
        self.assertEqual(num_solved, 1)
