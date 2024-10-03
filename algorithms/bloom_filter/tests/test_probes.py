
import hashlib
from unittest import skip, TestCase

import bloom_filter

from pprint import pprint
dump = pprint


class TestProbes(TestCase):
    def test_get_probes_using_random_stdlib(self):
        func = bloom_filter.get_probes_using_random_stdlib
        self._check_probes(func, 'James B Grossweiner', count=7, top=10_000)

    def test_get_probes_using_hash(self):
        func = bloom_filter.get_probes_using_hash
        self._check_probes(func, 'Yolanda Squatpump', count=7, top=10_000)

    def test_get_probes_using_hash_lengths(self):
        func = bloom_filter.get_probes_using_hash

        # 98-bits
        self._check_probes(func, 'Dan Gleebitz', count=7, top=10_000)

        # 493-bits
        self._check_probes(func, 'Emma Roids', count=17, top=500_000_000)


    def _check_probes(self, func, key, count, top):
        probes = func(key, count=count, top=top)
        num = 0
        for probe in probes:
            self.assertIsInstance(probe, int)
            self.assertGreaterEqual(probe, 0)
            self.assertLessEqual(probe, top)
            num += 1
        self.assertEqual(num, count)
