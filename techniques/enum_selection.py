"""
Experiment with randomly selecting one of several enum.
"""

from __future__ import annotations

from enum import auto, Enum
import random
from typing import Type

from pprint import pprint as pp


# Basic syntax
class Mood(Enum):
    STRESSED = auto()
    RELAXED = auto()


# Add alternative constructor
class Day(Enum):
    MONDAY = 1
    TUESDAY = 2
    WEDNESDAY = 3
    THURSDAY = 4
    FRIDAY = 5
    SATURDAY = 6
    SUNDAY = 7

    @classmethod
    def from_mood(cls, mood: Mood) -> Day:
        match mood:
            case Mood.STRESSED:
                return cls.MONDAY
            case Mood.RELAXED:
                return cls.SATURDAY
            case _:
                raise ValueError("Unknown mood")


# Create from iterable
Pet = Enum('Pet', ('ANT', 'BIRD', 'CAT', 'DOG', 'ELK', 'FROG'))


class RandomEnum:
    """
    Lazily unpack enumeration in order to select a random element.
    """
    def __init__(self, enumeration: Type[Enum]):
        self.enumeration = enumeration
        self.unpacked = None

    def __call__(self) -> Enum:
        if self.unpacked is None:
            self.unpacked = list(self.enumeration)
        return random.choice(self.unpacked)


if __name__ == '__main__':
    # Name and value
    print(f"{Pet.DOG.name = }")
    print(f"{Pet.DOG.value = }")

    # Dot or square-bracket syntax uses key
    print(f"{Pet.CAT = }")
    print(f"{Pet['CAT'] = }")

    # Call syntax uses value
    print(f"{Pet(3) = }")

    # Pick random day of week
    picker = RandomEnum(Day)
    print([picker() for _ in range(3)])

    print(f"{Day.from_mood(Mood.STRESSED) = }")
