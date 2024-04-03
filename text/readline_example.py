#!/usr/bin/env python3
"""
Use the standard library's readline module to provide word completion.
"""

from __future__ import annotations
import logging
import readline


# We can't print to console to debug, so we're logging instead
logging.basicConfig(
    format='%(message)s',
    filename='readline_example.log',
    filemode='w',
    level=logging.DEBUG,
)
logger = logging.getLogger(__name__)


# Lox language keywords to start with - we'll add identifiers as we go
keywords = [
    'and', 'class', 'clock', 'false', 'fun',
    'nil', 'or', 'print', 'true', 'var', 'while',
]


def input_loop(completer: Completer) -> None:
    while True:
        line = input('input> ')
        if line.casefold() in ('quit', 'exit'):
            break
        print(f">>> {line!r}")

        for word in line.split():
            completer.add(word)


class Completer:
    """
    Class-based completion function.
    """
    def __init__(self, words: list[str]|None) -> None:
        """
        Initialiser.

        Args:
            words:
                Initial set of words for completion list.
        """
        self.words = [] if words is None else words
        self.words.sort()

        # Current set of matches
        self._matches = []

    def add(self, word: str) -> None:
        """
        Add word to list of completions.
        """
        # Ignore repeats
        if word in self.words:
            return

        self.words.append(word)
        self.words.sort()

    def complete(self, text: str, state: int) -> str|None:
        """
        Callback function called by readline module.

        The readline module keeps calling this function with increasing
        values of `state` until a None is returned, signalling no more
        matches. For this reason we cache the current matches found.

        Args:
            text:
                Prefix to search for.
            state:
                Zero-based index of number of times function called for this
                match.

        Returns:
            Word
        """
        # Find possible matches on first call
        if state == 0:
            self._matches = self._find_matches(text)

        # Look-up and return next match
        response = None
        try:
            response = self._matches[state]
        except IndexError:
            pass
        logger.debug(f"complete({text!r}, {state}) => {response}")
        return response

    def _find_matches(self, text) -> list[str]:
        """
        Search words to generate list of matches.
        """
        # Empty match, return all
        if not text:
            return self.words[:]

        # Search by prefix
        matches = [word for word in self.words if word.startswith(text)]
        logger.debug(f"find_matches({text!r}) => {matches!r}")
        return matches


if __name__ == '__main__':
    completer = Completer(keywords)
    readline.set_completer(completer.complete)
    readline.parse_and_bind('tab: complete')
    input_loop(completer)
