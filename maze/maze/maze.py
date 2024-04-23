
from collections import namedtuple
from enum import auto, Flag
import logging
import random


logger = logging.getLogger(__name__)
Position = namedtuple('Position', 'x y')


class Cell(Flag):
    # Paths
    north = auto()
    east = auto()
    south = auto()
    west = auto()

    # Visited by algorithm?
    visited = auto()

    def as_text(self):
        content = '\u2588'          # Full block
        if self & self.visited:
            content = '\u2593'      # Dark shade
        content = self._value_
        return f'{content}'


class Maze:
    def __init__(self, width, height):
        self.cells = [[Cell(0) for y in range(height)] for x in range(width)]
        self.width = width
        self.height = height

    def fill(self):
        """
        Fill cells using Recursive backtracking algorithm.

        See: https://en.wikipedia.org/wiki/Maze_generation_algorithm
        """
        stack = []
        num_visited = 0
        num_cells = self.width * self.height

        # Start in top-left corner
        current = Position(0, 0)
        logger.info("Start at (%s, %s)", current.x, current.y)
        stack.append(current)

        while num_visited < num_cells:
            # Visit cell
            if not self.cells[current.x][current.y] & Cell.visited:
                self.cells[current.x][current.y] |= Cell.visited
                num_visited += 1

            # Move to next cell
            neighbours = self.get_neighbours(current)
            try:
                current = random.choice(neighbours)
                stack.append(current)
            except IndexError:
                current = stack.pop()
                logger.debug("Dead end reached. Backtrack to (%s, %s)", current.x, current.y)
            logger.debug("Move to (%s, %s)", current.x, current.y)

        logger.info("Finish at (%s, %s)", current.x, current.y)

    def get_neighbours(self, pos):
        """
        Return positions of not visited neighbours to given position.
        """
        neighbours = []

        def append_if_not_visited(neighbour):
            cell = self.cells[neighbour.x][neighbour.y]
            if not cell & Cell.visited:
                neighbours.append(neighbour)

        # North
        if pos.y > 0:
            neighbour = Position(pos.x, pos.y - 1)
            append_if_not_visited(neighbour)
        # East
        if pos.x < (self.width - 1):
            neighbour = Position(pos.x + 1, pos.y)
            append_if_not_visited(neighbour)
        # South
        if pos.y < (self.height - 1):
            neighbour = Position(pos.x, pos.y + 1)
            append_if_not_visited(neighbour)
        # West
        if pos.x > 0:
            neighbour = Position(pos.x - 1, pos.y)
            append_if_not_visited(neighbour)

        return neighbours

    def __repr__(self):
        lines = []
        for y in range(self.height):
            line = []
            for x in range(self.width):
                cell = self.cells[x][y]
                line.append(cell.as_text())
            lines.append(''.join(line))
        return '\n'.join(lines)
