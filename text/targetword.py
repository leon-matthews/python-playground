#!/usr/bin/env python3
"""
Solve Targetword puzzle.

    E O T
    S V O
    O H R

Find as many words as possible using the letters above. Every word must use
the centre letter. Letters may only be used once. All words must be at
least four letters long. There is at least one word that uses all nine
letters.

Copyright (C) 2021 by Leon Matthews <https://lost.co.nz/>
Released to the public-domain under the BSD Zero Clause License.
"""

import argparse
import itertools
from pathlib import Path
from pprint import pprint as pp
import sys
import time
from typing import Iterator


def find_permutations(required: str, remaining: str) -> Iterator[str]:
    """
    Generate all legal combinations of letters.
    """
    letters = list(remaining) + [required]
    for length in range(4, len(letters) + 1):
        for permutation in itertools.permutations(letters, length):
            if required not in permutation:
                continue
            word = ''.join(permutation)
            yield word


def load_wordlist(path: Path, encoding: str = 'utf-8') -> list[str]:
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


def new_york_times_spelling_bee(
    required: str,
    remaining: str,
    wordlist: list[str],
    min_length: int = 4
) -> set[str]:
    """
    Allow repeated.
    """
    # Solutions may only use these letters
    allowed = set(list(options.remaining) + [required])

    # Try every word in wordlist
    found = set()
    num_total = 0
    num_too_short = 0
    num_not_required = 0
    num_tried = 0
    for candidate in wordlist:
        num_total += 1

        # Skip words too short
        if len(candidate) < min_length:
            num_too_short += 1
            continue

        # Skip words not containing required letter
        if required not in candidate:
            num_not_required += 1
            continue

        num_tried += 1
        if set(candidate).issubset(allowed):
            found.add(candidate)

    print(num_total, num_too_short, num_not_required, num_tried)
    return found


def main(options: argparse.Namespace) -> None:
    """
    Script's entry point.
    Args:
        word_list_path:
            Path to word list to use.
    """
    start = time.perf_counter()

    # Try every word in wordlist
    wordlist = load_wordlist(options.wordlist)
    found = new_york_times_spelling_bee(options.required, options.remaining, wordlist=wordlist)

    for word in sorted(found):
        print(word)

    # Print summary to stderr
    elapsed = time.perf_counter() - start
    print(
        f"\n"
        f"Found {len(found):,} words from list "
        f"of {len(wordlist):,} words in {elapsed:.3f} seconds.",
        file=sys.stderr
    )


def parse(args: list[str]) -> argparse.Namespace:
    """
    Parse command-line arguments to produce set of options to give to `main()`.
    """
    description = "Solve Targetword puzzle."
    parser = argparse.ArgumentParser(description=description)
    default = '/usr/share/dict/words'

    parser.add_argument('required', metavar='REQUIRED')
    parser.add_argument('remaining', metavar='REMAINING')
    parser.add_argument(
        '-w', '--wordlist', metavar='FILE', type=Path, nargs='?', default=default,
        help=f"Path to a wordlist, defaults to {default}")
    return parser.parse_args(args)


if __name__ == '__main__':
    options = parse(sys.argv[1:])
    try:
        main(options)
        sys.exit(0)
    except (IOError, RuntimeError) as e:
        print(e, file=sys.stderr)
    sys.exit(1)
