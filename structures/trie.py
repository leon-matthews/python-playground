#!/usr/bin/env python3

from pprint import pformat, pprint as pp
import sys
from typing import Any


class Trie:
    """
    Simple nested-dictionary implementation of a Trie.

    Allows searching for prefixes and whole-word matches for a word-list.

    The overhead of the many dictionaries used causes memory usage to be
    higher than using a plain dictionary.

    Words are stored as lower-case, trim-ed strings in a nested dictionary.
    """
    def __init__(self):
        self._trie = {}

    @classmethod
    def from_file(cls, path):
        """
        Create new `Trie` object from words in the given path.
        """
        return cls.from_words(cls._read_file(path))

    @classmethod
    def from_words(cls, words):
        """
        Create new `Trie` object from given words.
        """
        trie = cls()
        trie._load(words)
        return trie

    def is_word(self, word):
        """
        Does the whole `word` exist in trie?
        """
        prefix = self._prefix(word)
        if prefix is False:
            return False

        # End of word?
        return True if None in prefix else False

    def is_prefix(self, word):
        """
        Is the given `word` found as prefix, or as whole word?
        """
        prefix = self._prefix(word)
        return bool(prefix)

    def prefixes(self, prefix):
        """
        Return all full words that start with `prefix`.
        """
        raise NotImplementedError
        words = []
        tree = self._prefix(prefix)
        if not tree:
            return words

        def generate_words(prefix, tree):
            for letter in tree:
                if letter is None:
                    continue

                word = prefix + letter
                if None in tree[letter]:
                    yield word
                else:
                    pp(tree[letter])
                    for x in generate_words(word, tree[letter]):
                        yield x


        for word in generate_words(prefix, tree):
            words.append(word)

        pp(words)
        return words

    def _count_dicts(self,) -> int:
        """
        Recursively count the number of nested dictionaries used by trie.

        Args:
            root:
                Dictionary to start with.

        Returns:
            Total number of dictionaries found.
        """
        def count(parent: dict[str, Any]) -> int:
            # Empty?
            num_dicts = 1
            if not parent:
                return num_dicts

            for child in parent.values():
                if isinstance(child, dict):
                    num_dicts += 1
                    num_dicts += count(child)
            return num_dicts

        return count(self._trie)


    def _load(self, words):
        """
        Replace current data with that from `words` iterable.
        """
        self._trie = {}
        for word in words:
            word = word.strip().lower()
            current = self._trie
            for letter in word:
                current = current.setdefault(letter, {})
            current[None] = None

    def _prefix(self, word):
        """
        Return sub-trie if `word` is a valid prefix, `False` otherwise.
        """
        current = self._trie
        for letter in word:
            if letter in current:
                current = current[letter]
            else:
                return False
        else:
            return current

    @staticmethod
    def _read_file(path):
        """
        Generater yielding lower-case words from file path.
        """
        with open(path, 'rt') as fp:
            for word in fp:
                yield word

    def __repr__(self):
        return pformat(self._trie)

    def __str__(self):
        lines = []
        trie = self._trie
        for letter in trie:
            children = trie[letter]
            lines.append(children)

        return '\n'.join(lines)


"""
def search_trie(word, trie):
    "
    Find word or prefix in trie.
    "
    def in_trie(trie, word):
...     current_dict = trie
...     for letter in word:
...         if letter in current_dict:
...             current_dict = current_dict[letter]
...         else:
...             return False
...     else:
...         if _end in current_dict:
...             return True
...         else:
...             return Fals
"""


if __name__ == '__main__':
    if len(sys.argv) != 2:
        print(f"usage: {sys.argv[0]} [WORD_LIST]", file=sys.stderr)
    else:
        trie = Trie.from_file(sys.argv[1])
        pp(trie._count_dicts())
