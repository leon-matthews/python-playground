#!/usr/bin/env python3

from itertools import cycle
from time import sleep
from sys import stdout

print("Hello... ", end='')

for c in cycle('🕐🕑🕒🕓🕔🕕🕖🕗🕘🕙🕚'):
    stdout.write(c)
    stdout.flush()
    sleep(0.2)
    stdout.write('\b\b')

