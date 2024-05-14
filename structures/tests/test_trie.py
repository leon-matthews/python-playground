
from pprint import pprint as pp
from unittest import skip, TestCase

from ..trie import Trie


class TestTrie(TestCase):
    words = (
        'apple',
        'applecart',
        'applecarts',
        'applejack',
        'applejacks',
        'apples',
        'applesauce',
        'applesauces',
    )

    def test_is_word(self):
        """
        Whole-word matches only
        """
        trie = Trie.from_words(self.words)

        pp(trie._count_dicts())

        self.assertFalse(trie.is_word('banana'))
        self.assertFalse(trie.is_word(''))

        self.assertTrue(trie.is_word('apple'))
        self.assertFalse(trie.is_word('appl'))

        self.assertTrue(trie.is_word('applejacks'))
        self.assertTrue(trie.is_word('applejack'))
        self.assertFalse(trie.is_word('applejac'))

    def test_is_prefix(self):
        trie = Trie.from_words(self.words)
        self.assertTrue(trie.is_prefix('a'))
        self.assertTrue(trie.is_prefix('ap'))
        self.assertTrue(trie.is_prefix('app'))
        self.assertTrue(trie.is_prefix('appl'))
        self.assertTrue(trie.is_prefix('apple'))

        self.assertFalse(trie.is_prefix('appleton'))
        self.assertFalse(trie.is_prefix('banana'))

    @skip('Not implemented')
    def test_prefixes(self):
        trie = Trie.from_words(self.words)

        words = trie.prefixes('b')
        self.assertEqual(words, [])

        words = trie.prefixes('apples')
        pp(words)
