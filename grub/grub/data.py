
from .utils import exponential_moving_average, OrdinaryLeastSquares


class Data:
    """
    Get the raw data ready for plotting.
    """
    def __init__(self, data, trend_days=7):
        """
        Initialiser.

        Args:
            data (iterable):
                An iterable 2-tuples: (date: datetime.date, weight: float)
        """
        dates = []
        weights = []
        for date,  weight in data:
            dates.append(date)
            weights.append(weight)

        # Plain lists of values
        self.dates = dates
        self.weights = weights

        # Mapping from index to weight
        smoothed = {}
        weights = exponential_moving_average(self.weights, (1.0/7.0))
        for index, weight in enumerate(weights, 1):
            smoothed[index] = weight
        self.smoothed = smoothed

        # Trend line
        self.slope, self.intercept = self.get_trend(trend_days)

    def get_target(self):
        """
        Return tomorrow's target weight.
        """
        last = list(self.smoothed.keys())[-1]
        return self.smoothed[last]

    def get_total(self):
        """
        Return the start to current difference inthe smoothed data.
        """
        keys = list(self.smoothed.keys())
        return self.smoothed[keys[-1]] - self.smoothed[keys[0]]

    def get_trend(self, num_days):
        """
        Return the best-fit line over the smoothed data, for the last n days.

        Intended as a small encouragement (or admonition!).

        Returns (tuple):
            Returns slope and intercept for straight line.
        """
        last_week = list(enumerate(self.smoothed.values(), 1))[-num_days:]
        slope, intercept = OrdinaryLeastSquares(last_week).calculate()
        return (slope, intercept)

    def get_smoothed(self):
        """
        Fetch all smoothed values.

        Returns (tuple):
            Returns x and y values: (x: list, y: list)
        """
        x = []
        y = []
        for index, average in enumerate(self.smoothed.values(), 1):
            x.append(index)
            y.append(average)
        return (x, y)

    def get_weights(self):
        """
        Fetch all weights.

        Returns (tuple):
            Returns x and y values: (x: list, y: list)
        """
        x = []
        y = []
        for index, weight in enumerate(self.weights, 1):
            x.append(index)
            y.append(weight)
        return (x, y)

    def get_weights_bad(self):
        """
        Fetch only the weights that were worse than the smoothed value.

        Returns (tuple):
            Returns x and y values: (x: list, y: list)
        """
        x = []
        y = []
        for index, weight in enumerate(self.weights, 1):
            smoothed = self.smoothed[index]
            if weight > smoothed:
                x.append(index)
                y.append(weight)
        return (x, y)

    def get_weights_good(self):
        """
        Fetch only the weights that were better or equal than the smoothed value.

        Returns (tuple):
            Returns x and y values: (x: list, y: list)
        """
        x = []
        y = []
        for index, weight in enumerate(self.weights, 1):
            smoothed = self.smoothed[index]
            if weight <= smoothed:
                x.append(index)
                y.append(weight)
        return (x, y)
