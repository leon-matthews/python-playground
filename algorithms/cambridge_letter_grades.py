"""
Use `bisect.bisect_right()` to find correct letter grade.

Interesting use of the bisect module - but we must be careful to use
`bisect_right()` and not `bisect_left()`, or we'd get very different results!
"""

import bisect
import sys
import unittest


def cambridge_grade(score: int) -> str:
    """
    Return letter-grade from percentage score.

        >>> cambridge_grade(69)
        'C'

    Args:
        score:
            Percentage grade.

    Raises:
        ValueError:
            If percentage outside of expected range.

    Returns:
        String for grade.
    """
    if score < 0 or score > 100:
        raise ValueError(f"Invalid percentage value: {score!r}")

    breakpoints = (30, 40, 50, 60, 70, 80, 90)
    grades = ('G', 'F', 'E', 'D', 'C', 'B', 'A', 'A*')
    i = bisect.bisect_right(breakpoints, score)
    return grades[i]


class CambridgeGradeTest(unittest.TestCase):
    def test_expected_range(self) -> None:
        self.assertEqual(cambridge_grade(0), 'G')
        self.assertEqual(cambridge_grade(29), 'G')
        self.assertEqual(cambridge_grade(30), 'F')
        self.assertEqual(cambridge_grade(39), 'F')
        self.assertEqual(cambridge_grade(40), 'E')
        self.assertEqual(cambridge_grade(49), 'E')
        self.assertEqual(cambridge_grade(50), 'D')
        self.assertEqual(cambridge_grade(59), 'D')
        self.assertEqual(cambridge_grade(60), 'C')
        self.assertEqual(cambridge_grade(69), 'C')
        self.assertEqual(cambridge_grade(70), 'B')
        self.assertEqual(cambridge_grade(79), 'B')
        self.assertEqual(cambridge_grade(80), 'A')
        self.assertEqual(cambridge_grade(89), 'A')
        self.assertEqual(cambridge_grade(90), 'A*')
        self.assertEqual(cambridge_grade(100), 'A*')

    def test_floating_point(self) -> None:
        self.assertEqual(cambridge_grade(69.99), 'C')       # type: ignore
        self.assertEqual(cambridge_grade(70.00), 'B')       # type: ignore

    def test_too_small(self) -> None:
        message = r"^Invalid percentage value\: -1$"
        with self.assertRaisesRegex(ValueError, message):
            cambridge_grade(-1)

    def test_too_large(self) -> None:
        message = r"^Invalid percentage value\: 101$"
        with self.assertRaisesRegex(ValueError, message):
            cambridge_grade(101)


if __name__ == '__main__':
    if len(sys.argv) == 1:
        unittest.main()
    else:
        for score in sys.argv[1:]:
            print(score, cambridge_grade(int(score)))
