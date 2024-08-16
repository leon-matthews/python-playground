#!/usr/bin/env python3

from collections import defaultdict
from pprint import pprint as pp
import sys

from matplotlib import pyplot


DATA = [
    ("2.6.9",         81_924,  1_655),
    ("2.7.18",       100_138,  1_769),
    ("3.0.1",         78_160,  1_613),
    ("3.1.5",         79_736,  1_162),
    ("3.2.6",         86_383,  1_207),
    ("3.3.7",         77_193,  1_268),
    ("3.4.10",        83_097,  1_816),
    ("3.5.10",        91_988,  1_032),
    ("3.6.15",        97_531,  2_306),
    ("3.7.17",       116_547,  2_206),
    ("3.8.18",       138_947,  1_205),
    ("3.9.18",       142_735,  2_604),
    ("3.10.12",      141_423,  5_128),
    ("3.11.5",       184_631,  2_563),
    ("3.12.4",       200_844,  3_405),
    ("3.13rc1",      205_381,  3_088),
    ("3.13rc1 +JIT", 218_255,  3_268),
    # ~ ("PyPy 7.3",   1_140_251, 44_726),
]


def main() -> int:
    # Prepare data
    data = defaultdict(list)
    for version, games_per_sec, stderr in DATA:
        data['version'].append(version)
        data['games_per_sec'].append(games_per_sec)
        data['stderr'].append(stderr)

    pp(data)

    # Create a visualization
    figure = pyplot.figure()
    plot(figure, data)
    pyplot.show()


if __name__ == '__main__':
    sys.exit(main())
