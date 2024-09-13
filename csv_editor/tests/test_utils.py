#!/usr/bin/env python3

"""
Simple unittest
"""

import doctest
import unittest

from csv_editor import utils
from csv_editor.utils import spreadsheet_index


def load_tests(loader, tests, ignore):
    """
    Add doctests to test suite.
    """
    doctests = doctest.DocTestSuite(utils)
    tests.addTests(doctests)
    return tests


class TestExcelIndexing(unittest.TestCase):
    def test_zero(self):
        self.assertEqual(spreadsheet_index(0), 'A')

    def test_single_digits(self):
        self.assertEqual(spreadsheet_index(0), 'A')
        self.assertEqual(spreadsheet_index(1), 'B')
        ...
        self.assertEqual(spreadsheet_index(24), 'Y')
        self.assertEqual(spreadsheet_index(25), 'Z')

    def test_transitions(self):
        self.assertEqual(spreadsheet_index(25), 'Z')
        self.assertEqual(spreadsheet_index(26), 'AA')
        self.assertEqual(spreadsheet_index(27), 'AB')
        ...
        self.assertEqual(spreadsheet_index(51), 'AZ')
        self.assertEqual(spreadsheet_index(52), 'BA')
        self.assertEqual(spreadsheet_index(53), 'BB')

    def test_invalid(self):
        with self.assertRaisesRegex(
                ValueError,
                r"invalid literal for int\(\) with base 10: 'banana'",
        ):
            spreadsheet_index('banana')
