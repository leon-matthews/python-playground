
import unittest

from .. import writer


class WriterTest(unittest.TestCase):

    def test_not_implemented(self):
        with self.assertRaises(NotImplementedError):
            writer.dump(42)
        with self.assertRaises(NotImplementedError):
            writer.dumps('Hello, world')
