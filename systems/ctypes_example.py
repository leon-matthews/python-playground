"""
Load a shared library on Linux and run some of its functions.
"""

from ctypes import cdll
import faulthandler
import random
import sys
from typing import Any


class LibC:
    """
    Load the system's C shared library and wrap a couple of its functions.
    """

    name = "libc.so.6"

    def __init__(self) -> None:
        """
        Initialiser.

        Also seeds the random number generator because the default is just
        terrible otherwise!
        """
        self.libc = cdll.LoadLibrary(LibC.name)
        self.srand()

    def printf(self, template: bytes, *args: Any) -> int:
        """
        Call system's C library printf() function.

        Note that printf prints to the real standard output channel, *not* to
        `sys.stdout`, so output will only work at the console prompt.

        Returns:
            The number of formatted bytes written.
        """
        num_bytes = self.libc.printf(template, *args)
        assert isinstance(num_bytes, int)
        return num_bytes

    def rand(self) -> int:
        """
        Generate random number using system's C library `rand()` function.

        See:
            man 3 rand

        Returns:
            Random-ish number.
        """
        random = self.libc.rand()
        assert isinstance(random, int)
        return random

    def srand(self, seed: int|None = None) -> None:
        """
        Seed system's C library random number generator.

        Call's the `srand()` function of same. I had forgotten how bad the libc
        random number generator is. It defaults to seeding its internal seed to
        one. Just the number one, every single time.

        Args:
            seed:
                Override seed, otherwise a random integer is used.

        See:
            man 3 rand

        Returns:
            Random-ish number.
        """
        if seed is None:
            seed = random.randint(0, sys.maxsize)
        self.libc.srand(seed)


if __name__ == '__main__':
    # Dump traceback if our use of ctypes makes Python crash.
    faulthandler.enable()

    # This may be the most stupid and convoluted way to roll a dice ever!
    libc = LibC()
    number = libc.rand() % 6 + 1
    num_bytes = libc.printf(b"You rolled a %d\n", number)
    print(f"({libc.name} printed {num_bytes} bytes to standard output)")
