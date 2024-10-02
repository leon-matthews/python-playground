
from collections import deque


def exponential_moving_average(data, smoothing=0.10):
    """
    Calculate the running EMA using geometric progression.

    TODO: Deal with missing data points:

            You can either  reuse the last computed EMA, or fill-forward the previous
            period's sample data and recompute the EMA.  I generally prefer the second
            option, which should cause a decay. Only go for the first option if your
            application won't change its logic based on missing data.

    Args:
        data: Raw input data
        smoothing (float): Weighting. Lower value is smoother.

    Returns:
        List of smoothed values
    """
    if not (smoothing > 0 and smoothing < 1):
        raise ValueError("smoothing must be between 0 and 1")

    previous = None
    averages = []
    for datum in data:
        if previous is None:
            previous = datum
        average = (smoothing * datum) + ((1-smoothing) * previous)
        averages.append(average)
        previous = average
    return averages


def simple_moving_average(data, period):
    """
    Return moving averages.

    Returns values even if window isn't yet full.
    """
    averages = []
    window = deque(maxlen=period)
    for d in data:
        window.append(d)
        average = sum(window) / len(window)
        averages.append(average)
    return averages


def skip_comments(line):
    """
    Return `False` if line is blank or starts with a '#'.

    Intended to be used with `filter()`, ie. `filter(skip_comments, file)`.
    """
    line = line.strip()
    if not line or line.startswith('#'):
        return False
    else:
        return True


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
        if len(data) < 2:
            raise ValueError("At least two points required to calculate a best fit")

        self.x = [x[0] for x in data]
        self.y = [y[1] for y in data]
        self.slope = None
        self.intercept = None

    def calculate(self):
        """
        Calculate best fit line using Ordinary Least Squares method.

        Returns (tuple):
            The slope and intercept as a 2-tuple: (slope: float, intercept: float)
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
