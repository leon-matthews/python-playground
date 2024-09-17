#!/usr/bin/env python3

"""
Test of Python 3 built-in functions as a learning exercise.

http://docs.python.org/3/library/functions.html
"""

from decimal import Decimal
from pprint import pprint as pp
from unittest import skip, TestCase


class AbsTest(TestCase):
    """
    Return the absolute value of a number.

        >>> abs(-17)
        17

    """
    def test_abs_integer(self):
        self.assertEqual(4, abs(4))
        self.assertEqual(4, abs(-4))

    def test_abs_complex(self):
        self.assertAlmostEqual(abs(complex(3, 4)), 5.0)
        self.assertAlmostEqual(abs(complex(3, -4)), 5.0)
        self.assertAlmostEqual(abs(complex(-3, 4)), 5.0)
        self.assertAlmostEqual(abs(complex(-3, -4)), 5.0)

    def test_abs_decimal(self):
        d = Decimal(-1.3)
        self.assertAlmostEqual(abs(d), Decimal('1.3'))

    def test_abs_raises_type_error(self):
        message = r"bad operand type for abs\(\): "
        with self.assertRaisesRegex(TypeError, message + "'str'"):
            abs('Banana')
        with self.assertRaisesRegex(TypeError, message + "'set'"):
            abs({-3, 5, 7})
        with self.assertRaisesRegex(TypeError, message + "'list'"):
            abs([-3, 5, 7])


class AllTest(TestCase):
    """
    Return True if no elements of given iterable are 'falsey'.
    """
    def test_all_empty_iterable(self):
        self.assertTrue(all(dict()))
        self.assertTrue(all(list()))
        self.assertTrue(all(set()))
        self.assertTrue(all(tuple()))

    def test_all_truthy(self):
        self.assertTrue(all([1, 'test', 4.2]))

    def test_all_falsey(self):
        self.assertFalse(all([1, 1, 1, 1, 1, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]))

    def test_all_raises_type_error(self):
        with self.assertRaisesRegex(TypeError, "'int' object is not iterable"):
            all(12)


class AnyTest(TestCase):
    """
    Return True if any element of the iterable is True.
    """
    def setUp(self):
        self.falsey = [False, 0, 0.0, '', dict(), list(), tuple()]

    def test_any_empty(self):
        self.assertFalse(any([]))

    def test_any_falsey(self):
        self.assertFalse(any(self.falsey))

    def test_any_truthy(self):
        falsey = self.falsey[:]
        falsey.append(True)
        self.assertTrue(any(falsey))

    def test_any_raises_type_error(self):
        with self.assertRaisesRegex(TypeError, "'int' object is not iterable"):
            any(12)


class AsciiTest(TestCase):
    """
    Like repr(), but escapes the non-ASCII characters in the string returned.
    """
    def test_ascii_quotes_added(self):
        self.assertEqual(ascii("Carrot"), "'Carrot'")

    def test_ascii_not_bytes(self):
        self.assertIsInstance(ascii('Zucchini'), str)
        self.assertNotEqual(ascii('Zucchini'), b'Zucchini')

    def test_ascii_other_types(self):
        self.assertEqual(ascii(43), '43')
        self.assertEqual(ascii(0.5), '0.5')
        self.assertEqual(ascii(['a', 3, True]), "['a', 3, True]")
        self.assertEqual(ascii({'a': 1, 'b': 2, 'c': 3}), "{'a': 1, 'b': 2, 'c': 3}")

    def test_ascii_unicode(self):
        self.assertEqual(ascii('café'), "'caf\\xe9'")


class BinTest(TestCase):
    def test_bin(self):
        """
        Convert an integer number to a binary string.
        bin(x)
        """
        self.assertEqual(bin(1), '0b1')
        self.assertEqual(bin(2), '0b10')
        self.assertEqual(bin(32), '0b100000')
        self.assertEqual(bin(255), '0b11111111')
        self.assertEqual(bin(1234567890), '0b1001001100101100000001011010010')


class BoolTest(TestCase):
    def test_bool(self):
        """
        Convert given value to a Boolean
        bool([x])
        """

        # False
        self.assertFalse( False )
        self.assertFalse( '' )
        self.assertFalse( 0 )
        self.assertFalse( 0.0 )
        self.assertFalse( list() )
        self.assertFalse( dict() )
        self.assertFalse( tuple() )
        self.assertFalse( set() )

        # True
        self.assertTrue( True )
        self.assertTrue( ' ' )
        self.assertTrue( 'test' )
        self.assertTrue( 42 )
        self.assertTrue( 0.0000000001 )


class ByteArrayTest(TestCase):
    def test_bytearray(self):
        """
        Return a new (mutable) array of bytes.
        bytearray([source[, encoding[, errors]]])
        """
        # Empty
        b = bytearray()
        b2 = repr(b)
        self.assertEqual(b2, "bytearray(b'')")

        # String constructor
        b = bytearray('Leon', encoding='utf-8')
        b2 = repr(b)
        self.assertEqual(b2, "bytearray(b'Leon')")


class BytesTest(TestCase):
    def test_bytes(self):
        """
        Return a new bytes object
        bytes([source[, encoding[, errors]]])
        """

        # Empty
        b = bytes()
        b2 = repr(b)
        self.assertEqual(b2, "b''")

        # String constructor
        b = bytes('Leon', encoding='utf-8')
        b2 = repr(b)
        self.assertEqual(b2, "b'Leon'")


class ChrTest(TestCase):
    def test_chr(self):
        """
        Return string of length one with the given Unicode codepoint
        chr(i)
        """
        self.assertEqual( 'A', chr(65) )
        self.assertEqual( 'a', chr(97) )


@skip('Too difficult')
class ClassMethodTest(TestCase):
    def test_classmethod(self):
        """
        Decorator that returns a class method for a function (decorator)
        classmethod(function)
        """
        raise NotImplementedError


@skip('Too difficult')
class CompileTest(TestCase):
    def test_compile(self):
        """
        Compile given source into a code or AST object
        compile(source, filename, mode, flags=0, dont_inherit=False)
        """
        raise NotImplementedError


class ComplexTest(TestCase):
    def test_complex(self):
        """
        Create a new complex number
        complex([real[, imag]])
        """

        c = complex( 3, 4)
        self.assertEqual( c, complex(3, 4) )
        self.assertEqual( 5.0, abs(c) )


@skip('Too boring')
class DelAttrTest(TestCase):
    def test_delattr(self):
        """
        Deletes the named attribute, provided the object allows it.
        delattr(object, name)
        """
        raise NotImplementedError


class DictTest(TestCase):
    def test_dict(self):
        """
        Create a new dictionary object'
        dict([arg])
        """
        d = dict()
        self.assertTrue( isinstance( d, dict ) )
        d2 = {}
        self.assertEqual( d, d2 )


class DirTest(TestCase):
    def test_dir(self):
        """
        Create data directory, optionally from given object
        dir([object])
        """
        self.assertEqual( ['self'], dir() )


class DivModTest(TestCase):
    def test_divmod(self):
        """
        Perform division, returning both quotient and remainder as a tuple.
        divmod(a, b)
        """
        value, remainder = divmod(95, 10)
        self.assertEqual( value, 9 )
        self.assertEqual( remainder, 5 )

        value, remainder = divmod(11.5, 5.0)
        self.assertEqual( value, 2.0 )
        self.assertEqual( remainder, 1.5 )


class EnumerateTest(TestCase):
    def test_enumerate(self):
        """
        Generates count, item tuple from iterable
        enumerate(iterable, start=0)
        """
        seasons = ['spring', 'summer', 'autumn', 'winter']
        output = []
        for count, season in enumerate(seasons):
            output.append('{} {}'.format( count, season ) )
        expected = ['0 spring', '1 summer', '2 autumn', '3 winter']
        self.assertEqual( output, expected )



@skip('Too difficult')
class EvalTest(TestCase):
    def test_eval(self):
        """
        Parse and evaluate Python expression
        eval(expression, globals=None, locals=None)
        """
        raise NotImplementedError


@skip('Too difficult')
class ExecTest(TestCase):
    def test_exec(self):
        """
        Dynamic excution of Python code
        exec(object[, globals[, locals]])
        """
        raise NotImplementedError


class FilterTest(TestCase):
    def test_filter(self):
        """
        Yield objects that for which given function return true
        filter(function, iterable)
        """
        numbers = (1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12)
        def is_even(a):
            return a % 2 == 0
        even = filter(is_even, numbers)
        even = repr(tuple(even))
        self.assertEqual(even, '(2, 4, 6, 8, 10, 12)')


class FloatTest(TestCase):
    def test_float(self):
        """
        Floating number constructor
        float([x])
        """
        f = float(3)
        self.assertEqual(f, 3.0)

        f = float('3.0')
        self.assertEqual(f, 3.0)

        # White space okay
        f = float('   3.0   ')
        self.assertEqual(f, 3.0)

        # Other non-numeric prefix not okay
        self.assertRaises(ValueError, float, '$3.00')

        # Other non-numeric suffixes not okay either
        self.assertRaises(ValueError, float, '3.00 is the price')

@skip('Test pending')
class PendingTest(TestCase):
    def test_format(self):
        """
        Convert a value to a string representation, as per format_spec.
        Note that format(value, spec) merely calls value.__format__(spec)
        format(value[, format_spec])
        """
        raise NotImplementedError

@skip('Test pending')
class FrozenTestTest(TestCase):
    def test_frozenset(self):
        """
        Return a frozenset object, optionally with elements taken from iterable.
        frozenset([iterable])
        """
        raise NotImplementedError

@skip('Test pending')
class GetAttrTest(TestCase):
    def test_getattr(self):
        """
        Return the value of the named attributed of object. name  must be a string.
        getattr(object, name[, default])
        """
        raise NotImplementedError


class GlobalsTest(TestCase):
    def test_globals(self):
        """
        Return a dictionary representing the current global symbol table.
        """
        g = globals()
        self.assertIn('__builtins__', g)
        self.assertIn('__doc__', g)
        self.assertIn('__file__', g)
        self.assertIn('__name__', g)
        self.assertIn('__package__', g)


@skip('Test pending')
class HasAttrTest(TestCase):
    def test_hasattr(self):
        """
        True if the string is the name of one of the object's attributes, False if not.
        hasattr(object, name)
        """
        raise NotImplementedError


@skip('Test pending')
class HashTest(TestCase):
    def test_hash(self):
        """
        Return the hash value of the object (if it has one). Hash values are integers.
        hash(object)
        """
        raise NotImplementedError


@skip('Interactive use only')
class HelpTest(TestCase):
    def test_help(self):
        """
        Invoke the built-in help system.
        This function is added to the built-in namespace by the site module.
        help([object])
        """
        raise NotImplementedError

class HexTest(TestCase):
    def test_hex(self):
        """
        Convert an integer to a hexadecimal string.
        hex(x)
        """
        self.assertEqual(hex(1), '0x1')
        self.assertEqual(hex(2), '0x2')
        self.assertEqual(hex(32), '0x20')
        self.assertEqual(hex(255), '0xff')
        self.assertEqual(hex(1234567890), '0x499602d2')


@skip('Test pending')
class IdTest(TestCase):
    def test_id(self):
        """
        Return the 'id' of an object.
        This is an integer which is guaranteed to be unique and constant for
        this object during its lifetime. Two objects with non-overlapping
        lifetimes may have the same id() value.
        id(object)
        """
        raise NotImplementedError


@skip('Interactive use only')
class InputTest(TestCase):
    def test_input(self):
        """
        Reads a line from input, converts it to a string.
        input([prompt])
        """
        raise NotImplementedError

class IntTest(TestCase):
    def test_int(self):
        """
        Convert a string or number to an integer, if possible
        int([number | string[, base]])
        """
        i = int(3)
        self.assertEqual(i, 3)

    def test_round_towards_zero(self) -> None:
        i = int(3.8)
        self.assertEqual(i, 3)
        i = int(-3.8)
        self.assertEqual(i, -3)

    def test_easy_strings(self) -> None:
        i = int('3')
        self.assertEqual(i, 3)

    def test_strings_in_different_bases(self) -> None:
        s = '101'
        i = int(s)
        self.assertEqual(i, 101)
        i = int(s, 2)
        self.assertEqual(i, 5)
        i = int('1001001100101100000001011010010', 2)
        self.assertEqual(i, 1234567890)

    def test_literal_flavours(self) -> None:
        i = 0b011
        self.assertEqual(i, 3)
        i = 0o11
        self.assertEqual(i, 9)
        i = 11
        self.assertEqual(i, 11)
        i = 0x11
        self.assertEqual(i, 17)

    def test_whitespace_strings(self) -> None:
        i = int('   3   ')
        self.assertEqual(i, 3)

    def test_fail_float_strings(self) -> None:
        self.assertRaises(ValueError, int, '3.0')

    def test_non_whitepace_prefix(self) -> None:
        self.assertRaises(ValueError, int, '$3')

    def test_non_whitepace_suffix(self) -> None:
        self.assertRaises(ValueError, int, '3 dollars is the price')


class IsInstanceTest(TestCase):
    def test_isinstance(self):
        """
        Is argument an instance of the given class, or of a thereof?
        isinstance(object, classinfo)
        """
        i = 42
        self.assertTrue(isinstance(i, int))
        j = 42 + 33j
        self.assertTrue(isinstance(j, complex))
        f = 42.0
        self.assertTrue(isinstance(f, float))
        s = 'Hello world!'
        self.assertTrue(isinstance(s, str))


class LenTest(TestCase):
    def test_valid_types(self) -> None:
        self.assertEqual(len("Banana"), 6)
        self.assertEqual(len({1, 1, 2, 3, 5, 8, 13}), 6)


class ListTest(TestCase):
    def test_iterable_to_list(self) -> None:
        self.assertEqual(list("Banana"), ['B', 'a', 'n', 'a', 'n', 'a'])


class LocalsTest(TestCase):
    def test_locals(self) -> None:
        fruit = 'Banana'
        self.assertEqual(locals().keys(), {'self', 'fruit'})


class MapTest(TestCase):
    def test_map(self) -> None:
        def power_of_two(n: int) -> int:
            return 2 ** n

        numbers = (1, 2, 3, 4, 5, 6, 7, 8)
        powers = list(map(power_of_two, numbers))
        self.assertEqual(powers, [2, 4, 8, 16, 32, 64, 128, 256])


class MaxTest(TestCase):
    def test_max(self) -> None:
        numbers = (11, 12, 31, 14, 15, 16, 17, 18)
        self.assertEqual(max(numbers), 31)

    def test_max_keyed(self) -> None:
        fruit = [
            'apple',
            'BANANA',
            'Cantaloupe',
        ]
        self.assertEqual(max(fruit), 'apple')
        self.assertEqual(max(fruit, key=str.casefold), 'Cantaloupe')


class MinTest(TestCase):
    def test_min(self) -> None:
        numbers = (11, 12, 31, 14, 15, 16, 17, 18)
        self.assertEqual(min(numbers), 11)

    def test_min_keyed(self) -> None:
        fruit = [
            'apple',
            'BANANA',
            'Cantaloupe',
        ]
        self.assertEqual(min(fruit), 'BANANA')
        self.assertEqual(min(fruit, key=str.casefold), 'apple')


class OctTest(TestCase):
    def test_oct(self) -> None:
        self.assertEqual(oct(256),  "0o400")

    def test_fail_oct(self) -> None:
        with self.assertRaises(TypeError):
            oct('256')


class OrdTest(TestCase):
    def test_ord(self) -> None:
        self.assertEqual(ord('A'), 65)
        self.assertEqual(ord('a'), 97)
        self.assertEqual(ord('€'), 8_364)
        self.assertEqual(ord('🐍'), 128_013)


class PowTest(TestCase):
    def test_pow(self):
        """
        Raise the first argument to the power of the second.
        """
        i = pow(2, 15)
        self.assertEqual(i, 32768)

    def test_pow_modulo(self) -> None:
        """
        Third argument calculates the modulo efficiently.
        """
        i = pow(2, 1024, 10)
        i2 = (2 ** 1024) % 10
        self.assertEqual(i, 6)
        self.assertEqual(i2, 6)
