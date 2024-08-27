#! /usr/bin/env python3

"""
Test Python client for Redis key-value store

2024 Update:
    The Redis database itself has switched to a proprietary software license.
    Various Open Source forks have sprung up, but it is not clear which one
    will emerge as the winner yet, but *Valkey* is looking good and is backed
    by the Linux Foundation.

See:
    https://redis.readthedocs.io/
    https://github.com/valkey-io/valkey
"""

from typing import Iterable

import redis


COUNT = 10
HOSTNAME = 'localhost'


db = redis.Redis(host=HOSTNAME, port=6379, socket_timeout=1)
print(db.ping())


# Use set() to overwrite string value over and again to same key
for i in range(COUNT):
    db.set('salutation', "Hello, world #{0}!".format(i))
print(db.get('salutation'))


def keygen(count: int) -> Iterable[str]:
    """
    Generator providing lots and lots of keys.
    """
    for i in range(count):
        yield f"salutation{i}"


# Use set() to write string values to different keys
for key in keygen(COUNT):
    greeting = f"Hello, world #{i}!"
    db.set(key, greeting)
print(key, db.get(key))


# Use get() to read greetings back
for key in keygen(COUNT):
    greeting = db.get(key)
print(greeting)


# Use pipeline to do it faster!
pipe = db.pipeline()
pipe.set('salutation 0', 'Hello 0')
pipe.set('salutation 1', 'Hello 1')
pipe.set('salutation 2', 'Hello 2')
print(pipe.execute())
