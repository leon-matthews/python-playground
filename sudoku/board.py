
from math import sqrt
from pprint import pprint as pp

from .exceptions import InvalidBoard, InvalidMove, SudokuError
from .render import draw_ascii


class Board:
    """
    Sudoku puzzle board.
    """
    width = 9
    box_width = int(sqrt(width))

    def __init__(self, clues):
        """
        Create puzzle and initialise with clues.

        Args:

        clues (list):
            A list of exactly size^2 numbers. ie. 81 for the normal size of nine.
            Zero is used for unknown cells. See the `utils` module for a
            collection of translation utilities.

        The `clues` array is copied into a new array `data`, which is used for
        holding the main working state. It is a single dimensional array of integers
        in the range from zero to `size`, inclusive. Zero is used for 'unknown'.
        """
        # Save a copy of original clues for later
        self._check_length(clues)
        self.clues = clues.copy()

        # Set current state of board
        self.data = self.clues.copy()

        # Check board (and build caches of box, column, and row data)
        self._boxes = {}
        self._columns = {}
        self._rows = {}
        self._validate()

    def get_value(self, row, column):
        """
        Get the value of the cell at the given coordinates.

        Returns (int): Raw value found. Zero indicates empty cell.
        """
        self._check_index(row)
        self._check_index(column)
        return self.data[self._get_data_index(row, column)]

    def is_solved(self):
        """
        Return `True` is board is solved.

        ie. Board is in a valid state, and there are no moves remaining.
        """
        self.validate()
        if self.unsolved() == 0:
            return True
        else:
            return False

    def set_value(self, row, column, value):
        """
        Set the value of the single cell at the given coordinates.

        Raises an `InvalidMove` exception if move is not possible.
        An `IndexError` or a `ValueError` are also possible if the arguments are
        out of bounds.

        Args:
            row (int): Zero-indexed row index.
            column (int): Zero-indexed column index.
            value (int): Value to assign to cell. Must be an integer <= board size.
        """
        # Check arguments
        if value <= 0 or value > self.width:
            message = f"Value must be an integer between 1 and {self.width}"
            raise ValueError(message)
        self._check_index(row)
        self._check_index(column)

        # Look for duplicates
        duplicates = []
        box_index = self._get_box_index(row, column)
        if value in self._boxes[box_index]:
            duplicates.append('box')
        if value in self._rows[row]:
            duplicates.append('row')
        if value in self._columns[column]:
            duplicates.append('column')

        # Throw exception
        if duplicates:
            joined = ' and '.join(duplicates)
            message = f"There is already a {value} in that {joined}"
            raise InvalidMove(message)

        # Set value, set cache
        data_index = self._get_data_index(row, column)
        self.data[data_index] = value
        self._boxes[box_index].add(value)
        self._rows[row].add(value)
        self._columns[column].add(value)

    def unsolved_count(self):
        """
        Return the count of cells still remaining to be solved.
        """
        return self.data.count(0)

    def __repr__(self):
        clues = ''.join([str(n) for n in self.clues])
        return f"<{self.__class__.__name__}({clues!r})>"

    def __str__(self):
        return draw_ascii(self)

    def _check_index(self, index):
        """
        Raise `IndexError` if given index is not in range [0, size-1]
        """
        if index < 0 or index >= self.width:
            message = f"Expecting an index from 0 to {self.width-1}"
            raise IndexError(message)

    def _check_length(self, data):
        """
        Ensure that length of data is correct.
        """
        expected = self.width ** 2
        if len(data) != expected:
            message = f"Expecting {expected} numbers, {len(data)} found."
            raise SudokuError(message)

    def _get_box(self, index):
        """
        Return list of values found in the box with the given index.

        Boxes are indexed left-to-right, top-to-bottom, starting with zero.

        Args:
            index (int): Box index, zero-based.

        Returns (list): Ordered list of integers found in box.
        """
        self._check_index(index)
        box_row, box_col = divmod(index, self.box_width)
        top_corner = (box_row * (self.box_width * self.width)) + (box_col * self.box_width)
        data = []
        for i in range(self.box_width):
            start = top_corner + (i * self.width)
            end = start + self.box_width
            data.extend(self.data[start:end])
        return data

    def _get_box_index(self, row, column):
        """
        Given cell coordinate, return the index of the box to which it belongs.

        Used as the argument for the `_get_box()` method.

        Args:
            column (int): Index of column, zero to size minus one.
            row (int): Index of row, zero to size minus one.
        """
        self._check_index(row)
        self._check_index(column)
        index = ((row  // self.box_width) * self.box_width) + (column // self.box_width)
        return index

    def _get_column(self, index):
        """
        Return list of cells in the column with the given index.

        Args:
            index (int): Column index, zero-based.

        Returns (list): Ordered list of integers found in column.
        """
        self._check_index(index)
        stride = self.width
        return self.data[index::stride]

    def _get_data_index(self, row, column):
        """
        Given cell coordinate, return its index into flat data array.

        eg. `data`, and `clues`.

        Args:
            column (int): Index of column, zero to size minus one.
            row (int): Index of row, zero to size minus one.
        """
        return (row * self.width) + column

    def _get_row(self, index):
        """
        Return list of cells in the row with the given index.

        Args:
            index (int): Row index, zero-based.

        Returns (list): Ordered list of integers found in row.
        """
        self._check_index(index)
        start = index * self.width
        end = start + self.width
        return self.data[start:end]

    def _validate(self):
        """
        Check that board is in a legal state, update all caches.

        Runs through all of the boxs, colunms, and rows looking for duplicates.

        Also rebuilds the `_boxes`, `_columns`, and  `_rows` data structures.
        These are sets that include only the real (ie. non-zero) values. They
        are used to quickly test for membership and check for duplicates. Each
        set is zero-indexed, as per the `get_box()` etc. methods.

        Raises a `InvalidBoard` exception if board data is not legal. Details
        of only the first duplicate is given in the exception message.
        """
        self._check_length(self.data)
        for i in range(self.width):
            # Check box
            box = self._get_box(i)
            data = [n for n in box if n]
            box_set = set(data)
            if len(data) != len(box_set):
                raise InvalidBoard(f"Duplicates found in box[{i}]: {box}")

            # Check column
            column = self._get_column(i)
            data = [n for n in column if n]
            column_set = set(data)
            if len(data) != len(column_set):
                raise InvalidBoard(f"Duplicates found in column[{i}]: {column}")

            # Check row
            row = self._get_row(i)
            data = [n for n in row if n]
            row_set = set(data)
            if len(data) != len(row_set):
                raise InvalidBoard(f"Duplicates found in row[{i}]: {row}")

            # Save sets for fast membership testing
            self._boxes[i] = box_set
            self._columns[i] = column_set
            self._rows[i] = row_set


class PencilMarked(Board):
    """
    Maintain a cache of all candicates for each cell.
    """
    def __init__(self, clues):
        super().__init__(clues)
        self.rebuild_cache()

    def candidates(self, column, row):
        """
        Calculate all possible values for the given cell.

        Returns: Empty list if already solved, otherwise a list of values.
        """
        return self._candidates[column][row]

    def rebuild_cache(self):
        """
        Rebuild entire cache.
        """
        self._candidates = [[{} for x in range(self.width)] for y in range(self.width)]
        print()
        pp(self._candidates)

        excluded = None# self.boxes[box] | self.rows[row] | self.columns[column]
        return list(set(range(1, 10)) ^ excluded)

        for row in range(self.width):
            for column in range(self.width):
                print((row * self.width) + column)

        pp(self._candidates)
