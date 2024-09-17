
from pprint import pprint as pp
import time
import unittest

from ..cities import Cities


class TestCities(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.cities = Cities()

    def test_get_item(self):
        """
        Match name exactly. Case is ignored.
        """
        city = self.cities['auckland']
        city2 = self.cities['Auckland']
        city3 = self.cities['AUCKLAND']

        self.assertTrue(city is city2 is city3)
        self.assertEqual(city.name, 'Auckland')
        self.assertEqual(city.iso3, 'NZL')
        self.assertAlmostEqual(city.latitude, -36.8481)
        self.assertAlmostEqual(city.longitude, 174.763)

    def test_get_item_unicode(self):
        """
        Exact match where name is definately not ASCII.
        """
        city = self.cities["Maḩmūd-e Rāqī"]
        city2 = self.cities['mahmud-e raqi']

        self.assertTrue(city is city2)
        self.assertEqual(city.iso3, 'AFG')
        self.assertEqual(city.name, 'Maḩmūd-e Rāqī')
        self.assertAlmostEqual(city.latitude, 35.0167)
        self.assertAlmostEqual(city.longitude, 69.3333)

    def test_get_item_missing(self):
        with self.assertRaisesRegex(KeyError, "'Narnia'"):
            self.cities['Narnia']

    def test_count(self):
        self.assertEqual(len(self.cities), 15_493)

    def test_search_unicode(self):
        def search(name):
            matches = self.cities.search(name)
            self.assertEqual(len(matches), 1)
            city = matches[0]
            self.assertEqual(city.name, 'São Paulo')
        search('sao paulo')
        search('são paulo')

    def test_search(self):
        """
        Sub-string search.
        """
        matches = self.cities.search('SAN PEDRO')
        self.assertEqual(len(matches), 6)
        self.assertEqual(matches[0].name, 'San Pedro')
        self.assertEqual(matches[-1].name, 'San Pedro de Ycuamandiyú')

    def test_search_single(self):
        matches = self.cities.search('Udon Thani')
        self.assertEqual(len(matches), 1)
        match = matches[0]
        self.assertEqual(match.name, 'Udon Thani')
        self.assertEqual(match.iso3, 'THA')
        self.assertAlmostEqual(match.latitude, 17.4048)
        self.assertAlmostEqual(match.longitude, 102.7893)

    def test_search_insensitive(self):
        matches = self.cities.search('village')
        self.assertEqual(len(matches), 44)
        matches = self.cities.search('Village')
        self.assertEqual(len(matches), 44)
        matches = self.cities.search('VILLAGE')
        self.assertEqual(len(matches), 44)
