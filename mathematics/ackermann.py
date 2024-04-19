#!/usr/bin/env python3

"""
Playing around with deep recursion and how using a cache affects
computability.

See:
    Inspired by the Computerphile video:
    The Most Difficult Program to Compute?
    https://www.youtube.com/watch?v=i7sm9dzFtEI

See:
    https://en.wikipedia.org/wiki/Ackermann_function
"""

from functools import lru_cache
from typing import Iterable


@lru_cache()
def ackermann(m, n):
    ackermann.num_calls += 1
    if m == 0:
        return n + 1

    if n == 0:
        return ackermann(m-1, 1)

    n_ = ackermann(m, n-1)
    answer = ackermann(m-1, n_)
    return answer

ackermann.num_calls: int = 0


def solvable() -> Iterable[tuple[int, int]]:
    """
    Yield (m,n) tuples that are actually practically solvable.
    """
    for m in range(5):
        for n in range(4):
            if m == 4 and n == 0:
                # ackermann(4, 1) == 65,533, and that is too much recursion!
                break
            yield (m, n)


if __name__ == '__main__':
    for m, n in solvable():
        print("ackerman({}, {}) = {}".format(m, n, ackermann(m, n)))
    print("ackermann() was called {:,} times".format(ackermann.num_calls))

    # Cache?
    if hasattr(ackermann, 'cache_info'):
        print(ackermann.cache_info())
