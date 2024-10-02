
import datetime
from os.path import dirname, isfile, join
from pprint import pprint as pp
from unittest import TestCase

from grub.log import Log, Record


DATA =  join(dirname(__file__), 'data')


class TestLog(TestCase):
    def test_file_not_found(self):
        path = '/no/such/file'
        self.assertFalse(isfile(path))
        with self.assertRaises(FileNotFoundError):
            Log(path)

    def test_read_log(self):
        path = join(DATA, 'dexter.log')
        self.assertTrue(isfile(path))
        log = Log(path)
        for record in log:
            self.assertIsInstance(record, Record)
            self.assertIsInstance(record.date, datetime.date)
            self.assertIsInstance(record.weight, float)
            self.assertIsInstance(record.note, str)

    def test_repr(self):
        path = join(DATA, 'dexter.log')
        log = Log(path)
        self.assertEqual(repr(log), "Log('dexter.log', encoding='utf-8')")
