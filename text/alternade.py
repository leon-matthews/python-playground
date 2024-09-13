#!/usr/bin/env python3

"""
Find pairs of words that 'alternade'.

Letters taken alternately from two words combine to produce a valid word.

For example:

    shoe + cold = schooled.

Requires: Python 3.8+

Copyright (C) 2021 by Leon Matthews <https://lost.co.nz/>
Released to the public-domain under the BSD Zero Clause License.
"""

import argparse
from pathlib import Path
import sys
import time
from typing import Dict, List, Set, Tuple


Alternades = Dict[str, Tuple[str, str]]


def find_alternades(words: Set[str]) -> Alternades:
    """
    Find all of the strict alternades from given word list.

        >>> find_alternades(...)
        {
            'sweaty': ('set', 'way'),
            'theorems': ('term', 'hoes'),
            'ballooned': ('blond', 'aloe'),
        }

    Args:
        words:
            Input word list, as a Python set.

    Returns:
        Dictionary keyed by the solution word, ordered by that word's length.
        The dictionary's values are 2-tuples with the first and second
        component words.
    """
    solutions = {}
    for word in words:
        first, second = word[::2], word[1::2]
        if (first in words) and (second in words):
            solutions[word] = (first, second)
    return solutions


def sort_alternades(unsorted: Alternades, reverse: bool = False) -> Alternades:
    """
    Sort output by word length, then the word itself

    Args:
        unsorted:
            A dictionary of alternade results.
        reverse:
            Reverse the default sort order.

    Returns:
        Sorted dictionary of alternades.
    """
    def length_then_alphabetical(word: str) -> Tuple[int, str]:
        length = len(word)
        if reverse:
            length = - length
        return length, word

    ranked = {}
    for word in sorted(unsorted, key=length_then_alphabetical):
        ranked[word] = unsorted[word]
    return ranked


def load_wordlist(path: Path, encoding: str = 'utf-8') -> List[str]:
    """
    Read wordlist from given path.

    File is assumed to contain one word per line, like the
    venerable file: '/usr/share/dict/words'

    Newlines and other whitespace is stripped and words are converted to
    lower-case.

    Args:
        path:
            Path to word list file, one line per word.

    Returns:
        List of words.
    """
    # Walrus operator used to catch blank lines with extraneous whitespace
    with open(path, 'rt', encoding=encoding) as fp:
        words = [
            stripped.casefold() for line in fp if (stripped := line.strip())
        ]
    return words


def main(options: argparse.Namespace) -> None:
    """
    Script's entry point.

    Args:
        word_list_path:
            Path to word list to use.

    """
    start = time.perf_counter()

    # Find solutions
    words = load_wordlist(options.wordlist)
    alternades = find_alternades(set(words))

    # Sort, then print results to stdout
    for word in sort_alternades(alternades, options.reverse):
        first, second = alternades[word]
        print(f"{first} + {second} = {word}")

    # Print summary to stderr
    elapsed = time.perf_counter() - start
    print(
        f"\n"
        f"Found {len(alternades):,} alternades from list "
        f"of {len(words):,} words in {elapsed:.3f} seconds.",
        file=sys.stderr
    )


def parse(args: List[str]) -> argparse.Namespace:
    """
    Parse command-line arguments to produce set of options to give to `main()`.
    """
    description = "Find alternades that exist in given wordlist"
    parser = argparse.ArgumentParser(description=description)
    default = '/usr/share/dict/words'
    parser.add_argument(
        'wordlist', metavar='FILE', type=Path, nargs='?', default=default,
        help=f"Path to a wordlist, defaults to {default}")
    parser.add_argument(
        '-r', '--reverse', action='store_true',
        help="Print longest solutions first")
    return parser.parse_args(args)


if __name__ == '__main__':
    options = parse(sys.argv[1:])
    try:
        main(options)
        sys.exit(0)
    except (IOError, RuntimeError) as e:
        print(e, file=sys.stderr)
    sys.exit(1)
