"""
Experiment with how Python represents type-annotated class attributes.

It is interesting the difference between class attributes that have a
value, and those that don't.

Note that it has only been since Python 3.10 that the `__annotations__`
attributes is guaranteed to be present and populated for class objects:
https://docs.python.org/3/howto/annotations.html
"""

from pprint import pprint as pp
from unittest import main, TestCase


class Base:
    empty: str
    value: str = 'apple'

    def function(self) -> None:
        pass


class Child(Base):
    pass


class BaseClassTest(TestCase):
    def test_attribute_access(self) -> None:
        """
        Try and access attributes using dot-notation.
        """
        # Fetch value as normal
        base = Base()
        self.assertEqual(base.value, 'apple')

        # Annotated-only attribute does not exist at runtime
        message = r"'Base' object has no attribute 'empty'"
        with self.assertRaisesRegex(AttributeError, message):
            base.empty

    def test_annotations(self) -> None:
        """
        Check contents of `__annotations__` class attribute.
        """
        # Note that functions are not included
        base = Base()
        expected = {
            'empty': str,
            'value': str,
        }
        self.assertEqual(expected, base.__annotations__)


class ChildClassTest(TestCase):
    """
    See if there are differences in child classes.
    """
    def test_attribute_access(self) -> None:
        """
        Try and access attributes using dot-notation.
        """
        # Fetch value as normal
        obj = Child()
        self.assertEqual(obj.value, 'apple')

        # Annotated-only attribute does not exist at runtime
        message = r"'Child' object has no attribute 'empty'"
        with self.assertRaisesRegex(AttributeError, message):
            obj.empty

    def test_annotations(self) -> None:
        """
        Check contents of `__annotations__` class attribute.
        """
        # Note that functions are not included
        obj = Child()
        expected = {
            'empty': str,
            'value': str,
        }
        self.assertEqual(expected, obj.__annotations__)


if __name__ == '__main__':
    main()
