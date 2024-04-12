#!/usr/bin/env python3

"""
Reservoir sampling.

Select a random element from a sequence of unknown length in only one pass.
"""
import random


def reservoir_samples(sequence, num_samples=10):
    """
    Use reservoir sampling to select a number of samples for any sequence.
    This works even when the sequence is too large to fit in memory, or its
    length is unknown.

    See: https://en.wikipedia.org/wiki/Reservoir_sampling

    sequence
        Sequence of elements with unknown length, ie. from generator.

    num_samples
        Number of samples to collect.
    """
    samples = []
    for index, element in enumerate(sequence):
        if index < num_samples:
            samples.append(element)
        else:
            # Replace elements with decreasing probability
            r = random.randint(0, index)
            if r < num_samples:
                samples[r] = element
    return samples


if __name__ == '__main__':
    import sys
    import timeit

    # Check arguments
    if len(sys.argv) == 2:
        path = sys.argv[1]
    else:
        print('usage: {} PATH'.format(sys.argv[0]))
        raise SystemExit(1)

    # Sample lines from text file
    with open(path, 'rt') as f:
        samples = reservoir_samples(f, num_samples=30)

    # Show results
    for line in sorted(samples):
        print(line.strip())
