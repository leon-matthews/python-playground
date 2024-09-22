#!/usr/bin/env python3
"""
Find words containining all vowels, in the correct order.
"""

from pathlib import Path
import re
import sys


WORDLIST_PATH = "../data/scrabble.txt"


def load_dictionary(path: Path) -> list[str]:
    """
    Get clean list of words from system wordlist
    """
    with open(path, 'rt') as fp:
        words = [word.strip().casefold() for word in fp]

    return words


def vowels_in_order(dictionary: list[str]) -> list[str]:
    """
    Strip the consonants, check against remainder
    """
    words = []
    for word in dictionary:
        vowels = re.sub(r'[^aeiou]', '', word)
        if vowels == 'aeiou':
            words.append(word)

    return words


def main() -> int:
    path = Path(WORDLIST_PATH)
    word_list = load_dictionary(path)
    words = vowels_in_order(word_list)
    print(words)
    return 0


if __name__ == '__main__':
    sys.exit(main())
