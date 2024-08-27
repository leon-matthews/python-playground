#!/usr/bin/env python3

"""
# Matplotlib

"Creating static, animated, and interactive visualizations"



## Axes interface (object-based, explicit)

Create a Figure and one or more Axes objects, then explicitly use methods on
these objects to add data, configure limits, set labels etc.

    figure, axes = pyplot.subplots()
    ax.plot(x, y)
    ax.set_title("Sample plot")
    pyplot.show()


## Pyplot interface (function-based, implicit)

Consists of functions in the pyplot module. Figure and Axes are manipulated
through these functions and are only implicitly present in the background.

    plt.plot(x, y)
    plt.title("Sample plot")
    plt.show()

"""

from collections import defaultdict
from pprint import pprint as pp
import sys

from matplotlib import pyplot, ticker


DATA = (
    ("2.6",           81_924,  1_655),
    ("2.7",          100_138,  1_769),
    ("3.0",           78_160,  1_613),
    ("3.1",           79_736,  1_162),
    ("3.2",           86_383,  1_207),
    ("3.3",           77_193,  1_268),
    ("3.4",           83_097,  1_816),
    ("3.5",           91_988,  1_032),
    ("3.6",           97_531,  2_306),
    ("3.7",          116_547,  2_206),
    ("3.8",          138_947,  1_205),
    ("3.9",          142_735,  2_604),
    ("3.10",         141_423,  5_128),
    ("3.11",         184_631,  2_563),
    ("3.12",         200_844,  3_405),
    ("3.13rc1",      205_381,  3_088),
    ("+ JIT", 218_255,  3_268),
    # ~ ("PyPy 7.3",   1_140_251, 44_726),
)

PYTHON_COLOURS = (
    '#4b8bbe',      # Cyan-Blue Azure
    '#306998',      # Lapis Lazuli
    '#ffe873',      # Shandy
    '#ffd43b',      # Sunglow
    '#646464',      # Granite grey
)


def plot(data):
    """
    Create visualisation.
    """
    py27_performance = 100_138

    colours = (
        [PYTHON_COLOURS[3]] * 2 +
        [PYTHON_COLOURS[1]] * 13 +
        [PYTHON_COLOURS[0]] * 2
    )
    x = data['version']
    y = data['games_per_sec']

    # Create figure & axes
    figure, axes = pyplot.subplots()

    # Hide all but bottom axes
    axes.spines["right"].set_visible(False)
    axes.spines["left"].set_visible(False)
    axes.spines["top"].set_visible(False)

    # ~ axes.set_xlabel("Python Version")
    # ~ axes.set_ylabel("Games per second")
    axes.get_yaxis().set_major_formatter(ticker.StrMethodFormatter('{x:,.0f}'))

    # Python v2.7
    # ~ axes.plot([x[0], x[-1]], [py27_performance, py27_performance], label="Baseline")

    # Plot performance vs version
    axes.bar(x, y, color=colours, yerr=data['stderr'])

    # Line to where we caught up with v2.7 performance
    axes.annotate(
        "Python 2.7",
        xy=(2, py27_performance + 5_000),
    )
    axes.axhline(
        y=py27_performance,
        xmin=0.15,
        xmax=0.525,
        color=PYTHON_COLOURS[4],
        dashes=(1, 2),
    )

    # Line to where we doubled v2.7 performance
    axes.annotate(
        "Twice Python 2.7",
        xy=(2, py27_performance * 2 + 5_000),
    )
    axes.axhline(
        y=py27_performance * 2,
        xmin=0.15,
        xmax=0.8,
        color=PYTHON_COLOURS[4],
        dashes=(1, 2),
    )

    # ~ axes.set_title("Python Performance by Version")
    #pyplot.savefig("by_version.png", dpi=150)
    pyplot.show()


def prepare_data():
    """
    Munge data into correct shape.
    """
    data = defaultdict(list)
    for version, games_per_sec, stderr in DATA:
        data['version'].append(version)
        data['games_per_sec'].append(games_per_sec)
        data['stderr'].append(stderr)

    return data


def set_fonts():
    """
    Override font defaults for matplotlib.
    """
    SIZE_DEFAULT = 14
    SIZE_LARGE = 16
    pyplot.rc("font", family="Noto Sans")
    pyplot.rc("font", weight="normal")
    pyplot.rc("font", size=SIZE_DEFAULT)
    pyplot.rc("axes", titlesize=SIZE_LARGE)
    pyplot.rc("axes", labelsize=SIZE_LARGE)
    pyplot.rc("xtick", labelsize=SIZE_DEFAULT)
    pyplot.rc("ytick", labelsize=SIZE_DEFAULT)


def main() -> int:
    data = prepare_data()
    plot(data)


if __name__ == '__main__':
    sys.exit(main())
