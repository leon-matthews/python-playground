#!/usr/bin/env python3
"""
Experiment with using LMDB (Lightning Memory-Mapped Database).

LMDB is a extremely fast key-value store, in the same solution space as Redis,
Berkley DB, or even (in the simple case) SQLite. Its data is kept in a folder
(not a single file) and is not portable between architectures. It has some nice
properties as a working store, if not for long-term storage.

From the LMDB Python-binding docs:

1. Ordered map interface (keys are always lexicographically sorted).
2. Reader/writer transactions: readers don’t block writers, writers don't
   block readers. Each environment supports one concurrent write transaction.
3. Read transactions are extremely cheap.
4. Environments may be opened by multiple processes on the same host, making it
   ideal for working around Python’s GIL.
5. Multiple named databases may be created with transactions covering all named
   databases.
6. Memory mapped, allowing for zero copy lookup and iteration. This is
   optionally exposed to Python using the buffer() interface.
7. Maintenance requires no external process or background threads.
8. No application-level caching is required: LMDB fully exploits the operating
   system’s buffer cache.

See:
    https://lmdb.readthedocs.io/en/release/
"""

import hashlib
import logging
from pathlib import Path
import time
from typing import Iterable

import lmdb


DATA_FOLDER = Path(__file__).parent.parent / 'data'
DATABASE = 'hashes.lmdb'
logger = logging.getLogger()
WORDLIST = DATA_FOLDER / 'scrabble.txt'


def words(path: Path) -> Iterable[str]:
    with open(path, 'rt', encoding='utf-8') as fp:
        for line in fp:
            yield line.strip()


def write(transaction: lmdb.Transaction, wordlist: Path) -> int:
    """
    Create mapping between every word in given list and its SHA1 hash.

    Args:
        transaction:
            LMDB transaction to run in.
        wordlist:
            Path to wordlist file.

    Returns:
        Count of records created.
    """
    count = 0
    started = time.perf_counter()
    for word in words(WORDLIST):
        key = word.encode('utf-8')
        value = hashlib.sha1(key).digest()
        transaction.put(key, value, dupdata=False, overwrite=False)
        count += 1

    elapsed = (time.perf_counter() - started) * 1_000
    logger.info(f"Wrote {count:,} records in {elapsed:.2f}ms")


def read_all(transaction: lmdb.Transaction) -> int:
    """
    Read back keys and values from given transaction.

    Args:
        transaction:
            LMDB transaction to run under.

    Returns:
        Count of records read.
    """
    cursor = transaction.cursor()
    count = 0
    started = time.perf_counter()
    for key, value in cursor:
        count += 1
        key = key.decode()
        # ~ print(value.hex(), key)

    elapsed = (time.perf_counter() - started) * 1_000
    logger.info(f"Read {count:,} records in {elapsed:.2f}ms")
    return count


if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG)

    env = lmdb.open(DATABASE)
    with env.begin(write=True) as transaction:
        write(transaction, WORDLIST)
        read_all(transaction)
