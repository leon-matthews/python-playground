

class SudokuError(RuntimeError):
    """
    Base class for all exceptions raised directly.
    """
    pass


class InvalidBoard(SudokuError):
    """
    Board is in an illegal state.
    """
    pass


class InvalidMove(SudokuError):
    """
    Board is in an illegal state.
    """
    pass
