
============
Bloom Filter
============

`(NZ native name could be Kowhai)`

This is my experiment is using bloom filter to increase the speed of database
look-ups.

What is it?
===========

    `Wikipedia <https://en.wikipedia.org/wiki/Bloom_filter>`_: A Bloom filter  is a
    space-efficient probabilistic data structure, conceived by Burton Howard Bloom in
    1970, that is used to test whether an element is a member of a set.

That is to say, it uses very little space to answer the question: `Have you seen this
before?`. It always answers either `no`, or `yes, probably...`.

False negatives are not possible. When a bloom filter says that it hasn't seen something
before, it really means it. False positives do happen however. There is a small
probability that when it says `yes` it is mistaken.  The more memory it is given, the
smaller that probability of error becomes.

Using one byte per item you can expect that `yes` to be incorrect about one time in
fifty or 2%. Going up to two bytes improves this dramatically: 1 in 2,000 or so. A nice
middle-ground might be 11-bits per item with an error rate of 1 in 200, or 0.5%.


Key Parameters
==============

There are four key parameters used when discussing a bloom filter:

#.  ``m``, the number of bits per element.
#.  ``n``, the total number of elements.
#.  ``p``, the expected false positive rate.
#.  ``k``, the optimal number of probes per element into bitarray.


The false-positive / space trade-off
====================================

.. todo:: There is also a performance trade-off, as more hashes need to be calculated.

.. code-block:: python

    def calculate_p(bits_per_element):
        return math.exp( - bits_per_element * math.pow(math.log(2), 2))

=============  ===============  ==========
bits per item  false positives  reciprocal
=============  ===============  ==========
6              5.60%            1 in 18
7              3.46%            1 in 29
8              2.14%            1 in 47
9              1.32%            1 in 75
10             0.82%            1 in 122
11             0.51%            1 in 197
12             0.31%            1 in 319
13             0.19%            1 in 516
14             0.12%            1 in 834
15             0.07%            1 in 1,349
16             0.05%            1 in 2,180
17             0.03%            1 in 3,525
18             0.02%            1 in 5,700
19             0.01%            1 in 9,215
=============  ===============  ==========
