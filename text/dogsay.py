#!/usr/bin/env python3

"""
Selects random ascii art picture from text file.

Individual pieces of ascii art are seperated from each other by one or more
blank lines.
"""

from pathlib import Path
import random
import re
import sys


ASCII_ART_FILE = Path("dogsay.txt")


def fetch_dogs(path: Path) -> list[str]:
    text = open('dogsay.txt', encoding='ascii').read()
    dogs = re.split('\n\n+', text)
    return dogs


def replace(dog: str, message: str) -> str:
    """
    Add message for dog to say.

    Args:
        message:
            Message to print

    Raises:
        ValueError:
            If string to print is too long.
    """
    old = "REPLACE"
    if len(message) > len(old):
        raise ValueError(f"Max message length is {len(old)}, given: {message!r}")
    else:
        message = f"{message:^{len(old)}}"

    dog = dog.replace(old, message)
    return dog


def main(message: str, path: Path|None = None) -> None:
    if path is None:
        path = ASCII_ART_FILE

    dogs = fetch_dogs(path)
    dog = random.choice(dogs)
    dog = replace(dog, message)
    print(dog)


if __name__ == '__main__':
    if len(sys.argv) == 1:
        main("Woof?")
    elif len(sys.argv) == 2:
        main(sys.argv[1])
    else:
        print(f"usage: {sys.argv[0]} [MESSAGE]", file=sys.stderr)
        sys.exit(1)
