#!/usr/bin/env python3

from collections import defaultdict
import sys

from matplotlib import pyplot, ticker


DATA = (
    ("Pi Zero",    2_430,   2_430),
    ("Pi 3B+",     7_720,  30_200),
    ("Pi Zero 2",  9_200,  36_400),
    ("Pi 4B",     30_400, 118_000),
    ("Pi 5B",     83_300, 333_000),
)

RPI_COLOURS = (
    '#c7053d',      # Raspberry Pi Shiraz
    '#8cc04b',      # Raspberry Pi Sushi
)


def plot(data):
    # Create figure & axes
    figure, axes = pyplot.subplots()

    # Hide all but bottom axes
    axes.spines["right"].set_visible(False)
    axes.spines["left"].set_visible(False)
    axes.spines["top"].set_visible(False)

    # Format axes
    # ~ axes.set_title("Raspberry Pi Single Core")
    # ~ axes.set_xlabel("Raspberry Pi Board")
    axes.set_ylabel("Games per second")
    axes.get_yaxis().set_major_formatter(ticker.StrMethodFormatter('{x:,.0f}'))

    # Data
    x = data['version']
    y = data['single_core']
    y2 = data['multi_core']

    # Plot!
    axes.bar(x, y2, color=RPI_COLOURS[1], label="Multi-core")
    axes.bar(x, y, color=RPI_COLOURS[0], label="Single core")
    axes.legend(loc="upper left")
    pyplot.show()
    # ~ pyplot.savefig("pi_single.png", dpi=300)


def prepare_data():
    """
    Munge data into correct shape.
    """
    data = defaultdict(list)
    for version, single, multi in DATA:
        data['version'].append(version)
        data['single_core'].append(single)
        data['multi_core'].append(multi)
    return data


def main() -> int:
    data = prepare_data()
    plot(data)


if __name__ == '__main__':
    sys.exit(main())
