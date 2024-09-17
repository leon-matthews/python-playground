"""
Latitude and longitude data for world cities.
"""

from collections import ChainMap, namedtuple
import csv
from difflib import SequenceMatcher
import gzip
import logging
from pathlib import Path
from pprint import pprint as pp
import time
import unicodedata


City = namedtuple('City', 'iso3 name latitude longitude')
logger = logging.getLogger(__name__)


def force_ascii(string):
    """
    Force string to ASCII-friendly string.
    """
    string = unicodedata.normalize('NFKD', string)
    string = string.encode('ASCII', 'ignore').decode('ASCII')
    return string


class Cities:
    """
    Global cities latitude/longitude database.

    You can treat it as a mapping. Note that the key is case-insensitive, and
    we do our best to deal with ASCII spellings::

        >>> cities = Cities()
        >>> cities['Auckland']
        City(iso3='NZL', name='Auckland', latitude=-36.8481, longitude=174.763)
        >>> cities['bazarak']
        City(iso3='AFG', name='Bāzārak', latitude=35.3129, longitude=69.5152)
        >>> cities['Narnia']
        ...
        KeyError: 'Narnia'

    Or do a substring search::

        >>> cities.search('Pedro')
        [
            City(iso3='ARG', name='San Pedro',
                 latitude=-24.2196, longitude=-64.87),
            ...
            City(iso3='PRY', name='San Pedro de Ycuamandiyú',
                 latitude=-24.09, longitude=-57.08),
        ]
        >>> cities.search('Narnia')
        []

    Reads an external datafile during initialisation, which it expects to find
    in the same folder as the this module.
    """
    data_file = 'cities.csv.gz'

    def __init__(self):
        self.cities = self._read_data_file()
        self._cities_mapping = None

    @property
    def cities_mapping(self):
        """
        Cities keyed by lower-cased name.
        """
        if self._cities_mapping is None:
            by_name = {x.name.lower(): x for x in self.cities}
            by_ascii = {force_ascii(k).lower(): v for k, v in by_name.items()}
            self._cities_mapping = ChainMap(by_name, by_ascii)
        return self._cities_mapping

    def search(self, query):
        """
        Return list of matching cities, best-matches first.
        """
        # Filter by sub-string
        needle = query.lower()
        candidates = []
        for city in self.cities:
            name = city.name.lower()
            name_ascii = force_ascii(city.name).lower()
            if (needle in name) or (needle in name_ascii):
                candidates.append(city)

        # Order by match ratio
        s = SequenceMatcher(a=needle)

        def match_ratio(city):
            s.set_seq2(city.name.lower())
            return s.ratio()

        candidates.sort(key=match_ratio, reverse=True)
        return candidates

    def _read_data_file(self):
        """
        Read compressed city data into a list of `City` named tuples.
        """
        folder = Path(__file__).resolve().parent
        path = folder / self.data_file
        logger.debug('Reading city data from: % s', path)
        cities = []
        start = time.perf_counter()
        with gzip.open(path, 'rt') as fp:
            reader = csv.reader(fp)
            for row in reader:
                city = City(
                    iso3=row[0],
                    name=row[1],
                    latitude=float(row[2]),
                    longitude=float(row[3]),
                )
                cities.append(city)
        elapsed = round((time.perf_counter() - start) * 1000)
        logger.debug(f"Loaded {len(cities):,} city locations in {elapsed}ms")
        return cities

    def __getitem__(self, name):
        """
        Find city using its exact name.

        Case insensitive, unicode normalised.
        """
        key = name.lower()
        try:
            return self.cities_mapping[key]
        except KeyError:
            pass
        raise KeyError(name)

    def __len__(self):
        return len(self.cities)
