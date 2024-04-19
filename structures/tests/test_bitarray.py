
from unittest import TestCase

from ..bitarray import BitArray


class TestBitArray(TestCase):
    def test_empty(self):
        b = BitArray(0)
        self.assertEqual(len(b), 0)
        self.assertEqual(b.num_bytes(), 0)

    def test_num_bytes(self):
        self.assertEqual(BitArray(72).num_bytes(), 9)
        self.assertEqual(BitArray(73).num_bytes(), 10)
        self.assertEqual(BitArray(80).num_bytes(), 10)
        self.assertEqual(BitArray(81).num_bytes(), 11)

    def test_get(self):
        b = BitArray(10)
        self.assertEqual(b[10], False)

    def test_get_index_error(self):
        b = BitArray(10)
        with self.assertRaises(IndexError):
            b[11]

    def test_iterate(self):
        b = BitArray(7)
        b[2] = True
        b[3] = True
        b[5] = True
        values = list(b)
        self.assertEqual(values, [False, False, True, True, False, True, False, False])

    def test_iter_string(self):
        b = BitArray(9)
        lines = []
        for line in b.iter_string():
            lines.append(line)
        self.assertEqual(lines, ['00000000', '0'])

    def test_len(self):
        b = BitArray(50)
        self.assertEqual(len(b), 50)

    def test_primes_to_50(self):
        """
        Primes to 100 using only 13 bytes of storage and the Sieve of Eratosthenes.
        """
        # Generate
        sieve = BitArray(100)
        small = [2, 3, 5, 7]
        sieve[1] = True
        for prime in small:
            # Mark all composite cells as true
            for i in range(0, len(sieve) + 1, prime):
                sieve[i] = True
            sieve[prime] = False

        # Bit pattern (
        bit_pattern = ''.join(sieve.iter_string())
        expected = (
            '01010011110101110111010101011111110111110111010111'
            '01111111010111011101110111110111110111111111010001'
        )
        self.assertEqual(bit_pattern, expected)

        # Back to integers
        self.assertEqual(sieve.num_bytes(), 13)
        primes = [num for num, x in enumerate(sieve) if x is False]
        expected = [
            2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47,
            53, 59, 61, 67, 71, 73, 79, 83, 89, 97,]
        self.assertEqual(primes, expected)

    def test_set_one(self):
        b = BitArray(10)
        self.assertEqual(b[7], False)
        b[7] = True
        self.assertEqual(b[7], True)
        b[7] = False
        self.assertEqual(b[7], False)

    def test_set_more(self):
        b = BitArray(12)
        b[0] = True
        b[2] = True
        b[12] = True
        for i in range(12):
            if i in [0, 2, 12]:
                self.assertTrue(b[i])
            else:
                self.assertFalse(b[i])

    def test_set_index_error(self):
        b = BitArray(10)
        b[0] = True
        b[10] = True
        with self.assertRaises(IndexError):
            b[11] = True

    def test_repr(self):
        b = BitArray(1000)
        r = repr(b)
        self.assertEqual(len(r), 79)
        self.assertTrue(r.startswith('<BitArray:000000000'))

    def test_str(self):
        b = BitArray(100)
        s = str(b)
        self.assertTrue(s.startswith('000000000000000000000'))
