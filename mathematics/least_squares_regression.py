
import unittest


class OrdinaryLeastSquares:
    """
    Calculate Ordinary Least Square regression.

    This is a simple straight-line best-fit line, where the line is given by
    the equation::

        y = mx + b

        'm' is the slope
        'x' is the independent variables
        'b' is intercept

    https://en.wikipedia.org/wiki/Ordinary_least_squares
    """

    def __init__(self, data):
        """
        Initialise with data set.

        Args:
            data (list): List of 2-tuples. The independent variable should be
                         first, the dependent variable second.
        """
        self.x = [x[0] for x in data]
        self.y = [y[1] for y in data]
        self.slope = None
        self.intercept = None

    def calculate(self):
        """
        Calculate best fit line using Ordinary Least Squares method.

        Returns (float):
            The slope and intercept as a 2-tuple.
        """
        x_mean = sum(self.x) / len(self.x)
        y_mean = sum(self.y) / len(self.y)
        numerator = 0.0
        denominator = 0.0
        for x, y in zip(self.x, self.y):
            numerator += (x - x_mean) * (y - y_mean)
            denominator += ((x - x_mean) ** 2)

        self.slope = numerator / denominator
        self.intercept = y_mean - (self.slope * x_mean)
        return (self.slope, self.intercept)

    @property
    def ssr(self):
        """
        sum of squared residuals (SSR
        Calculate the sum of squared errors (SSE) of the dependent variable.
        """
        if self.slope is None or self.intercept is None:
            raise ValueError('best fit has not yet been calculated')

        ssr = 0.0
        for x, y in zip(self.x, self.y):
            predicted_y = (self.slope * x) + self.intercept
            error = y - predicted_y
            ssr += error ** 2
        return ssr


class TestOrdinaryLeastSquare(unittest.TestCase):
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


if __name__ == '__main__':
    unittest.main()
