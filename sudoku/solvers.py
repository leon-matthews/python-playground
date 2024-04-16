"""
http://www.angusj.com/sudoku/hints.php
https://www.sudokuoftheday.com/techniques/
"""


from .render import draw_unicode


def single_candidates(puzzle):
    """
    Solve all of the single candidates currently visible.
    """
    solved = 0
    new_data = puzzle.data.copy()
    for row in range(puzzle.size):
        for column in range(puzzle.size):
            candidates = puzzle.candidates(column, row)
            if len(candidates) == 1:
                index = puzzle.index(column, row)
                new_data[index] = candidates[0]
                solved += 1

    if solved > 0:
        puzzle.data = new_data
        puzzle.rebuild()

    return solved


def single_candidates_all(puzzle):
    """
    Repeatedly run `single_candidates()` until no more can be found.
    """
    print()
    print(draw_unicode(puzzle))
    total = 0
    num_iterations = 1
    while True:
        num_solved = single_candidates(puzzle)
        total += num_solved
        if num_solved == 0:
            break
        print(f"{num_solved} cells solved, {puzzle.unsolved()} remaining")
        print(draw_unicode(puzzle))
        num_iterations += 1
    print(f"{num_iterations} iterations total")
    return total
