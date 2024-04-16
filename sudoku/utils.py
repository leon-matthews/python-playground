
import re


def import_string(string):
    """
    Convert given string into a list of numbers.

    Can happily import the output of `render.draw_ascii()` by simply
    dropping all formatting characters and allowing the use of
    full-stops in the place of zeros.

    Returns (list): List of integers found in string.
    """
    cleaned = string.lower()
    cleaned = re.sub('[^0-9a-z\.]', '', cleaned)
    numbers = []
    for c in cleaned:
        if c == '.':
            n = 0
        else:
            n = int(c)
        numbers.append(n)
    return numbers


def import_unicode(string):
    """
    Import numbers from a board output by `render.draw_unicode()`.
    """
    empty_cell = r'[║│]   (?=[║│])'
    cleaned = re.sub(empty_cell, '.', string)
    return import_string(cleaned)
