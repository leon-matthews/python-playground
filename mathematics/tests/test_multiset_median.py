
from collections import Counter
import statistics
from unittest import TestCase

from ..multiset_median import multiset_median


class CounterMedianTest(TestCase):
    def test_empty(self) -> None:
        message = r""
        with self.assertRaisesRegex(ValueError, message):
            multiset_median(Counter())

    def test_easy_example(self) -> None:
        numbers = [3, 3, 3, 6, 7, 9, 9]
        c = Counter(numbers)
        self.assertEqual(statistics.median(numbers), 6)
        self.assertEqual(multiset_median(c), 6)

    def test_high_low_error(self) -> None:
        message = r"^Only one of the high and low arguments may be true$"
        with self.assertRaisesRegex(ValueError, message):
            multiset_median(Counter(), high=True, low=True)

    def test_high_low(self) -> None:
        numbers = [1, 3, 5, 7]

        self.assertEqual(statistics.median_low(numbers), 3)
        self.assertEqual(statistics.median(numbers), 4.0)
        self.assertEqual(statistics.median_high(numbers), 5)

        c = Counter(numbers)
        self.assertEqual(multiset_median(c, low=True), 3)
        self.assertEqual(multiset_median(c), 4.0)
        self.assertEqual(multiset_median(c, high=True), 5)

    def test_no_repeats(self) -> None:
        squares = [1, 4, 9, 16, 25, 36, 49, 64, 81]
        c = Counter(squares)
        self.assertEqual(statistics.median(squares), 25)
        self.assertEqual(multiset_median(c), 25)

    def test_interpolation(self) -> None:
        n = [5, 5, 1, 5, 1, 5, 3, 3, 5, 3, 5, 5, 3, 1, 5, 5, 3, 3, 3, 5]
        self.assertEqual(statistics.median(n), 4.0)
        c = Counter(n)
        self.assertEqual(c.most_common(), [(5, 10), (3, 7), (1, 3)])
        self.assertEqual(multiset_median(c), 4.0)

    def test_large(self) -> None:
        count = 100_000_000
        c = Counter(
            {3: count, 5: count, 7: count, 11: count, 13: count, 17: count, 19: count}
        )
        self.assertEqual(c.total(), 7 * count)
        self.assertEqual(multiset_median(c), 11)
