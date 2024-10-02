
from pprint import pprint as pp
from unittest import TestCase

from grub.utils import (
    exponential_moving_average,
    OrdinaryLeastSquares,
    simple_moving_average,
)


class TestSimpleMovingAverage(TestCase):
    def test_empty(self):
        data = []
        averages = simple_moving_average(data, period=5)
        self.assertEqual(averages, [])

    def test_equal_values(self):
        data = [10, 10, 10, 10, 10, 10, 10, 10, 10, 10]
        averages = simple_moving_average(data, period=5)
        self.assertEqual(data, averages)

    def test_data(self):
        data = [
            67.50, 66.50, 66.44, 66.44, 66.25, 65.88, 66.63, 66.56, 65.63, 66.06,
            63.94, 64.13, 64.50, 62.81, 61.88, 62.50, 61.44, 60.13, 61.31, 61.38,
        ]
        expected = [
            67.50, 67.00, 66.81, 66.72, 66.63, 66.50, 66.52, 66.52, 66.43, 66.39,
            66.03, 65.79, 65.60, 65.24, 64.80, 64.46, 63.94, 63.30, 62.87, 62.40,
        ]
        averages = simple_moving_average(data, period=10)
        for a, e in zip(averages, expected):
            self.assertAlmostEqual(a, e, delta=0.01)


class TestExponentialMovingAverage(TestCase):
    def test_empty(self):
        data = []
        averages = exponential_moving_average(data, smoothing=0.10)
        self.assertEqual(averages, [])

    def test_equal_values(self):
        data = [10, 10, 10, 10, 10, 10, 10, 10, 10, 10]
        averages = exponential_moving_average(data, smoothing=0.10)
        self.assertEqual(data, averages)

    def test_too_real(self):
        data = [134.6, 132.8, 132.5]
        averages = exponential_moving_average(data, smoothing=0.10)

    def test_smoothing_too_high(self):
        message = "smoothing must be between 0 and 1"
        with self.assertRaisesRegex(ValueError, message):
            exponential_moving_average([], smoothing=1.0)

    def test_smoothing_too_low(self):
        message = "smoothing must be between 0 and 1"
        with self.assertRaisesRegex(ValueError, message):
            exponential_moving_average([], smoothing=0.0)


class TestOrdinaryLeastSquare(TestCase):
    @classmethod
    def setUpClass(cls):
        # Years of experience vs. annual salary.
        cls.salary = [
            (2, 15),
            (3, 28),
            (5, 42),
            (13, 64),
            (8, 50),
            (11, 58),
            (16, 90),
            (1, 8),
            (9, 54),
        ]

    def test_calculate(self):
        r = OrdinaryLeastSquares(self.salary)
        slope, intercept = r.calculate()
        self.assertAlmostEqual(slope, 4.79, delta=0.01)
        self.assertAlmostEqual(intercept, 9.18, delta=0.01)

    def test_calculate_ssr_value_error(self):
        r = OrdinaryLeastSquares(self.salary)
        error = "best fit has not yet been calculated"
        with self.assertRaisesRegex(ValueError, error):
            r.ssr()

    def test_calculate_ssr(self):
        r = OrdinaryLeastSquares(self.salary)
        r.calculate()
        self.assertAlmostEqual(r.slope, 4.79, delta=0.01)
        self.assertAlmostEqual(r.intercept, 9.18, delta=0.01)
        self.assertAlmostEqual(r.ssr, 245.31, delta=0.01)
