
from pprint import pprint as pp

from geolite2.db import BlockIP4, City, Country

from .data import DataTestCase


class DataTest(DataTestCase):
    """
    Confirm that data from `DataTestCase` is what we expect.
    """
    def test_block_ip4(self):
        """
        Examine 'block_ip4' table.
        """
        self.session.echo = True
        blocks = self.session.query(BlockIP4).all()
        self.assertEqual(len(blocks), 3)

        # Firsts
        self.assertEqual(
            [b.first for b in blocks],
            [3232235776, 3232236032, 3232236288],
        )

        # Lasts
        self.assertEqual(
            [b.last for b in blocks],
            [3232236031, 3232236287, 3232236543],
        )

    def test_city(self):
        city = self.session.query(City).first()
        self.assertEqual(city.id, 1)
        self.assertEqual(city.name, 'Auckland')
        self.assertEqual(city.time_zone, 'Pacific/Auckland')
        self.assertAlmostEqual(city.latitude, -36.8483)
        self.assertAlmostEqual(city.longitude, 174.7625)
        self.assertEqual(city.country.name, 'New Zealand')

    def test_country(self):
        country = self.session.query(Country).first()
        self.assertEqual(country.id, 1)
        self.assertEqual(country.name, 'New Zealand')
        self.assertEqual(country.iso3166, 'NZ')
