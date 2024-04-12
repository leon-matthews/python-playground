
from unittest import TestCase

from ..least_squares_regression import OrdinaryLeastSquares


class TestOrdinaryLeastSquare(TestCase):
    """
    Using data from worked example found in:
    https://towardsdatascience.com/linear-regression-simplified-ordinary-least-square-vs-gradient-descent-48145de2cf76
    """

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
