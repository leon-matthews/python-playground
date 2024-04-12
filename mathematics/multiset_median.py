#!/usr/bin/env python3

from collections import Counter
import math


def multiset_median(
    counter: Counter[int],
    *,
    high: bool = False,
    low: bool = False,
) -> float:
    """
    Efficiently determine the median of counter where the keys are numbers.

    Calculates the median *without* unpacking the counter into a sequence and
    passing it to a library function. Uses the same 'mean of middle two' method
    that the standard library's `statistics` package uses, with the option to
    use the high or low median instead.

    Args:
        high:
            Use the high median rather than the 'mean of middle two'. Value
            returned will be in set.
        low:
            As per `high`, but the low median instead.

    Raises:
        ValueError:
            If input is empty.
        ValueError:
            If both high and low arguments are true.

    Returns:
        Median value.
    """
    if high and low:
        raise ValueError("Only one of the high and low arguments may be true")

    # Find median values
    middle = (counter.total() + 1) / 2
    lower_pos = int(math.floor(middle))
    upper_pos = int(math.ceil(middle))
    lower_value = upper_value = None
    count = 0

    for key in sorted(counter.keys()):
        count += counter[key]
        if lower_value is None and count >= lower_pos:
            lower_value = key
        if upper_value is None and count >= upper_pos:
            upper_value = key
            break

    if lower_value is None or upper_value is None:
        raise ValueError("Cannot calculate median of empty Counter")

    # Median present, no interpolation needed
    if lower_pos == upper_pos:
        return lower_value

    # Pick your flavour! Middle-of-two, High, or Low median.
    if high:
        return upper_value
    elif low:
        return lower_value
    else:
        return (lower_value + upper_value) / 2
