
import unittest

from ..countries import Countries


class TestCountries(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.countries = Countries()

    def test_count(self):
        self.assertEqual(len(self.countries), 249)

    def test_get_item(self):
        """
        Match name exactly. Case is ignored.
        """
        country = self.countries['NZL']
        country2 = self.countries['nzl']
        self.assertTrue(country is country2)
        self.assertEqual(country, 'New Zealand')

    def test_get_item_not_found(self):
        with self.assertRaises(KeyError):
            self.countries['abc']
