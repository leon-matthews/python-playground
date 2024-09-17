
import dataclasses
from os.path import abspath, dirname, join
from pathlib import Path
from pprint import pprint as pp
from unittest import TestCase

from geolite2.csv import NamedTupleReader


class Coerced:
    """
    Coerce the types of a dataclass's fields.

    When empty, the field's defaults are used.
    """
    def __post_init__(self):
        for field in dataclasses.fields(self.__class__):
            raw = getattr(self, field.name)
            value = field.type(raw) if raw else field.default
            setattr(self, field.name, value)


@dataclasses.dataclass
class Price(Coerced):
    id: int
    size: str
    price: float = 0.00


DATA_FOLDER = abspath(join(dirname(__file__), 'files'))


pp(Price('2326', 'Large', '34.7392'))
pp(Price('2327', 'Medium', None))
pp(Price('2327', 'Medium'))
pp(Price('2327', 'Medium'))


class NamedTupleReaderTest(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        path = Path(DATA_FOLDER) / 'test_data.csv'
        with open(path, 'rt') as fp:
            reader = NamedTupleReader(fp)
            cls.rows = [row for row in reader]

    def test_named_tuple_reader(self):
        self.assertEqual(len(self.rows), 3)
        first = self.rows[0]
        self.assertEqual(first._fields, ('line', 'id', 'size', 'price'))
        self.assertEqual(tuple(first), (2, '2326', 'Large', '34.7392'))

        last = self.rows[-1]
        self.assertEqual(tuple(last), (4, '2324', 'Small', '20.950'))
