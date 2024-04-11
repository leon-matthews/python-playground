#!/usr/bin/env python3

"""
Estimates the area of a quarter circle, and hence PI, by random point samples.

Silly, but fun - and a nice illustration of the central limit theorem.
"""

import math
import random


def throw_darts(num_darts: int) -> float:
    """
    Estimate pi by throwing darts and counting those that land in a circle.

    Uses the Pythagorean theorem to test whether our point sample lands inside a
    quarter circle with a radius of one. Using a unit radius avoids having
    to caluclate a square root which is vital for performance.

    Args:
        num_darts:
            How many darts to throw.

    Returns:
        Estimate of pi, from ratio of darts in and out of a unit circle.
    """
    in_circle = 0
    for darts in range(1, num_darts + 1, 1):
        x = random.random()
        y = random.random()
        if x*x + y*y <= 1.0:
            in_circle += 1
    pi = 4 * (in_circle / float(num_darts))
    return pi


if __name__ == '__main__':
    num_darts = 1_000_000
    runs = 10

    guesses = []
    for _ in range(runs):
        pi = throw_darts(num_darts)
        print("Estimate after {:,} samples: {:0.8f}".format(num_darts, pi))
        guesses.append(pi)
    mean = sum(guesses) / len(guesses)
    print()
    print(f"Estimate mean of the {runs:,} trials:   {mean:0.8f}")
    print(f"Actual value of pi:               {math.pi:0.8f}")

    error_percentage = (abs(mean - math.pi) / math.pi) * 100
    print(f"                      Error is:   {error_percentage:.4f}‰")
