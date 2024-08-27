
from ipaddress import IPv4Network
from pprint import pprint as pp
from unittest import TestCase

from geolite2 import db
from geolite2.utils import calculate_range

from .data import create_block_ipv4, DataTestCase, TransactionTestCase


class FindTest(DataTestCase):
    def test_find_ipv4_succeeded(self):
        """
        Find a single IP address within the 'block_ip4' table.
        """
        data = db.find(self.session, '192.168.2.5')
        self.assertIsInstance(data, db.GeoIP2)
        self.assertEqual(data._asdict(), {
            'city': 'Auckland',
            'country': 'New Zealand',
            'iso3166': 'NZ',
            'latitude': -36.8483,
            'longitude': 174.7625,
            'time_zone': 'Pacific/Auckland'
        })

    def test_find_ipv4_boundaries(self):
        self.assertEqual(db.find(self.session, '192.168.0.255'), None)
        self.assertEqual(db.find(self.session, '192.168.1.0').city, 'Wellington')
        self.assertEqual(db.find(self.session, '192.168.1.255').city, 'Wellington')
        self.assertEqual(db.find(self.session, '192.168.2.0').city, 'Auckland')
        self.assertEqual(db.find(self.session, '192.168.2.255').city, 'Auckland')
        self.assertEqual(db.find(self.session, '192.168.3.0').city, 'Wellington')
        self.assertEqual(db.find(self.session, '192.168.3.255').city, 'Wellington')
        self.assertEqual(db.find(self.session, '192.168.4.0'), None)

    def test_find_ipv4_failed(self):
        ip = 1234567890
        data = db.find(self.session, ip)
        self.assertTrue(data is None)


class BlockIP4Test(TransactionTestCase):
    def test_add_minimal(self):
        """
        Create a minimally valid IPv4 block record - no city or country.
        """
        minimal_block = create_block_ipv4('192.168.1.0/24')
        self.session.add(minimal_block)
        self.session.commit()
        self.assertEqual(minimal_block.id, 1)

        block = self.session.query(db.BlockIP4).get(1)
        self.assertEqual(block.id, 1)
        self.assertEqual(block.first, 3232235776)
        self.assertEqual(block.last, 3232236031)
        self.assertEqual(block.city_id, None)
        self.assertEqual(block.country_id, None)

    def test_add_with_country(self):
        nz = db.Country(name='New Zealand', iso3166='NZ')
        country_block = create_block_ipv4('192.168.2.0/24', nz)
        self.session.add(country_block)
        self.session.commit()
        self.assertEqual(country_block.id, 1)

        block = self.session.query(db.BlockIP4).get(1)
        self.assertEqual(block.id, 1)
        self.assertEqual(block.first, 3232236032)
        self.assertEqual(block.last, 3232236287)
        self.assertEqual(block.city_id, None)
        self.assertEqual(block.country_id, 1)
        self.assertEqual(block.country.name, 'New Zealand')
