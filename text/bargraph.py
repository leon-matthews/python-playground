#! /usr/bin/env python3

import contextlib
from os import get_terminal_size
import random
import sys
import time


EIGHTHS = {
    0: '',
    1: '\u258F',
    2: '\u258E',
    3: '\u258D',
    4: '\u258C',
    5: '\u258B',
    6: '\u258A',
    7: '\u2589',
}


def build_bar(width: int) -> str:
    """
    Build bar of the given width using Unicode eigth-width bar characters.
    """
    full, remainder = divmod(width, 8)
    blocks = '\u2588' * full
    partial = EIGHTHS[remainder]
    return f"{blocks}{partial}"


@contextlib.contextmanager
def hide_cursor():
    print('\033[?25l', end="")
    try:
        yield
    finally:
        print('\033[?25h', end="")


if __name__ == '__main__':
    max_width, _ = get_terminal_size()
    max_width *= 8
    width = 0
    while width < max_width:
        with hide_cursor():
            print(build_bar(width), end="\r")
            sys.stdout.flush()
            width += random.randint(0, 16)
            time.sleep(0.1)
