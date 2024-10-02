
import matplotlib.dates as mdates


def plot(figure, data, num_days=None):
    """
    Plot data.

    Args:
        figure (`matplotlib.figure.Figure`):
            A `Figure` object - either to show interactively or to save as image.
        data (Data):
            A populated instance of Data.
        num_days (int|None):
            Number of days of data to plot. If None, all data will be plotted.

    Returns (`matplotlib.figure.Figure`):
        Populated figure object.
    """
    # Dates
    days_locator = mdates.DayLocator()      # every day
    days_format = mdates.DateFormatter('%Y-%m-%d')

    # Create figure
    axes = figure.add_subplot(1, 1, 1)
    axes.set_title("Leon's diet")
    axes.set_ylabel('Weight (kg)')

    # Raw weights: good and bad
    axes.plot(*data.get_weights_bad(), '^r')
    axes.plot(*data.get_weights_good(), 'vg')

    # Smoothed
    axes.plot(*data.get_smoothed(), ':k')

    # TODO: Best-fit trend arrow
    # ~ axes.arrow(0, 0, 0.5, 0.5, head_width=0.05, head_length=0.1, fc='k', ec='k')

    return figure
