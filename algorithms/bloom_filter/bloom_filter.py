"""
Bloom Filter

Raymond Hettinger

http://code.activestate.com/recipes/577684-bloom-filter/

Space efficient, probabilistic set membership tester. Has no False Negatives
but allows a rare False Positive.
"""


"""
Microbenchmarking
=================

SHA-1 digest to integer
-----------------------

1) int.from_bytes()

    >>> digest = '3cead5069d8fea36676b1353c78afa51056af0d1'
    >>> b = bytes.fromhex(digest)

    # (native) little-endian
    >>> import sys
    >>> sys.byteorder
    'little'
    >>> int.from_bytes(digest, 'little')
    404 nsec per loop

    # big endian
    >>> int.from_bytes(digest, 'big')
    404 nsec per loop

    # Hoist function call
    >>> from_b = int.from_bytes
    >>> from_b(b, 'little')
    296 nsec per loop

2) int constructor

    >>> digest = '3cead5069d8fea36676b1353c78afa51056af0d1'
    >>> int(digest, 16)
    608 nsec per loop


Divide and modulo big integer into lots of little ones

    >>> i = 347776377793920247910451207417170056546890739921
    >>> a, b = divmod(i, 32767)
    424 nsec per loop

"""

import logging
import hashlib
import math
from pprint import pprint;
from random import Random
from sys import byteorder
from time import perf_counter


dump = pprint
logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.DEBUG)


class BloomFilter:
    @staticmethod
    def calculate_parameters(num_elements, error_rate=None, megabytes=None):
        def log(num, bits):
            megabytes = num * bits / 1024 / 1024
            logger.info(f"Using {bits}-bits per element, expected size {megabytes} MiB")

        if error_rate is None and megabytes is None:
            bits_per_element = 11
            log(num_elements, bits_per_element)

    def __init__(self, num_bytes, num_probes, iterable=()):
        self.array = bytearray(num_bytes)
        self.num_probes = num_probes
        self.num_bins = num_bytes * 8
        self.update(iterable)

    def get_probes(self, key):
        random = Random(key).random
        return (int(random() * self.num_bins) for _ in range(self.num_probes))

    def update(self, keys):
        for key in keys:
            for i in self.get_probes(key):
                self.array[i//8] |= 2 ** (i%8)

    def __contains__(self, key):
        return all(self.array[i//8] & (2 ** (i%8)) for i in self.get_probes(key))


def get_probes_using_hash(key, *, count, top):
    """
    Generate probe locations from key, by extracting bits from its hash.

    Will raise a `RuntimeError` if not enough bits are available. This is unlikely
    in practice. The current limit is 512-bits, allowing for filters with one billion
    elements and a very generous 20-bits per element.

    Args:
        key (string): String to hash.
        count (int): Number of probes required.
        top (int): Top of range, ie. the largest value that will be returned.

    Timing:
        $ python3 -m timeit \
          -s "from bloom_filter import get_probes_using_hash as get_probes" \
          "list(get_probes('Heywood U. Cuddleme', count=11, top=1000))"

        top=1,000:         3.91 usec per loop
        top=100,000:       4.14 usec per loop
        top=10,000,000:    4.11 usec per loop
        top=1,000,000,000: 4.09 usec per loop

    Returns:
        An iterable of integer probe locations, of length `num`.
    """
    # Choose hash function
    min_bits = top.bit_length()
    total_bits = count * min_bits
    if total_bits <= 160:
        hash_function = hashlib.sha1
    elif total_bits <= 512:
        hash_function = hashlib.blake2b
    else:
        raise RuntimeError("Too many probes for hash function")

    # Build large integer
    key_bytes = key.encode('utf-8')
    hash_bytes = hash_function(key_bytes).digest()
    number = int.from_bytes(hash_bytes, 'little')

    # Bite off pieces
    mask = (2 ** min_bits) - 1
    probes = []
    for _ in range(count):
        probes.append((number & mask) % top)
        number >>= min_bits
    return probes


def get_probes_using_random_stdlib(key, *, count, top):
    """
    Timing:
        $ python3 -m timeit \
          -s "from bloom_filter import get_probes_using_random_stdlib as get_probes"

        top=1,000:          24.3 usec per loop
        top=100,000:        25.1 usec per loop
        top=10,000,000:     25.4 usec per loop
        top=1,000,000,000:  24.4 usec per loop
    """
    randrange = Random(key).randrange
    return (randrange(0, top+1) for _ in range(count))


def get_probes_using_random_xorshift(key, *, num, bits):
    raise NotImplementedError()


def test_probes_fram_hash():
    bytestring = 'Leon Matthews'.encode('utf-8')

    hash_ = hashlib.sha1(bytestring)
    start = perf_counter()
    sha1 = hashlib.sha1
    for _ in range(12):
        hash_ = sha1(hash_.digest())
        number = int.from_bytes(hash_.digest(), byteorder)
        probes = get_probes(number, 9, 33)
        print(probes)

    print(1_000_000 / (perf_counter() - start))


def bloom_filter_parameters():
    def calculate_p(bits_per_element):
        return math.exp( - bits_per_element * math.pow(math.log(2), 2))

    def k_from_p(p):
        return math.ceil(-(math.log(p, 2)))

    for num_elements in [1000, 100_000, 10_000_000, 1_000_000_000]:
        bits_per_element = 20
        heading = f"{num_elements:,} elements, {bits_per_element}-bits per element"
        print("="*len(heading))
        print(heading)
        print("="*len(heading))

        bits_total = (num_elements * bits_per_element)
        bits_per_probe = bits_total.bit_length()
        gigabytes = bits_total / 8 / 1e9
        p = calculate_p(bits_per_element)
        r = math.floor(1/p)
        k = k_from_p(p)
        memory = f"{gigabytes:.1f} GB RAM: {bits_per_element:>2} bits per element"
        suffix = "-" * (80-len(memory))
        print(memory, suffix)
        print(f"{k} probes of {bits_per_probe} bits each. {bits_per_probe*k} hash bits needed")
        print(f"False positives: 1 in {r:d}")
        print()






##  Sample application  ##############################################

class SpellChecker(BloomFilter):

    def __init__(self, wordlistfiles, estimated_word_count=125000):
        num_probes = 14           # set higher for fewer false positives
        num_bytes = estimated_word_count * num_probes * 3 // 2 // 8
        wordlist = (w.strip() for f in wordlistfiles for w in open(f))
        BloomFilter.__init__(self, num_bytes, num_probes, wordlist)

    def find_misspellings(self, text):
        return [word for word in text.lower().split() if word not in self]


## Example of subclassing with faster probe functions ################

from hashlib import sha224, sha256

class BloomFilter_4k(BloomFilter):
    # 4Kb (2**15 bins) 13 probes. Holds 1,700 entries with 1 error per 10,000.

    def __init__(self, iterable=()):
        BloomFilter.__init__(self, 4 * 1024, 13, iterable)

    def get_probes(self, key):
        h = int(sha224(key.encode()).hexdigest(), 16)
        for _ in range(13):
            yield h & 32767     # 2 ** 15 - 1
            h >>= 15

class BloomFilter_32k(BloomFilter):
    # 32kb (2**18 bins), 13 probes. Holds 13,600 entries with 1 error per 10,000.

    def __init__(self, iterable=()):
        BloomFilter.__init__(self, 32 * 1024, 13, iterable)

    def get_probes(self, key):
        h = int(sha256(key.encode()).hexdigest(), 16)
        for _ in range(13):
            yield h & 262143    # 2 ** 18 - 1
            h >>= 18


if __name__ == '__main__':

    ## Compute effectiveness statistics for a 125 byte filter with 50 entries

    from random import sample
    from string import ascii_letters

    states = '''Alabama Alaska Arizona Arkansas California Colorado Connecticut
        Delaware Florida Georgia Hawaii Idaho Illinois Indiana Iowa Kansas
        Kentucky Louisiana Maine Maryland Massachusetts Michigan Minnesota
        Mississippi Missouri Montana Nebraska Nevada NewHampshire NewJersey
        NewMexico NewYork NorthCarolina NorthDakota Ohio Oklahoma Oregon
        Pennsylvania RhodeIsland SouthCarolina SouthDakota Tennessee Texas Utah
        Vermont Virginia Washington WestVirginia Wisconsin Wyoming'''.split()

    bf = BloomFilter(num_bytes=125, num_probes=14, iterable=states)

    m = sum(state in bf for state in states)
    print('%d true positives and %d false negatives out of %d positive trials'
          % (m, len(states)-m, len(states)))

    trials = 100000
    m = sum(''.join(sample(ascii_letters, 8)) in bf for i in range(trials))
    print('%d true negatives and %d false positives out of %d negative trials'
          % (trials-m, m, trials))

    c = ''.join(format(x, '08b') for x in bf.array)
    print('Bit density:', c.count('1') / float(len(c)))


    ## Demonstrate a simple spell checker using a 125,000 word English wordlist

    from glob import glob
    from pprint import pprint

    # Use the GNU ispell wordlist found at http://bit.ly/english_dictionary
    checker = SpellChecker(glob('data/wordlists/english.?'))
    pprint(checker.find_misspellings('''
        All the werldz a stage
        And all the mehn and wwomen merrely players
        They have their exits and their entrances
        And one man in his thaim pllays many parts
        His actts being sevven ages
    '''))
