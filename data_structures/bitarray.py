
import math


class BitArray:
    def __init__(self, length):
        self.length = length
        self.data = bytearray(math.ceil(self.length/8))

    def iter_string(self):
        """
        Iterate over data as string, formatted as ascii, one byte at a time.

        eg. '10001011', '00001000', '1010'

        Note that depending on the length of the BitArray, the last part
        may be less than 8 characters long.
        """
        last, fragment = divmod(self.length, 8)
        for index, byte in enumerate(self.data):
            string = format(byte, '0>8b')
            if index == last:
                string = string[:fragment]
            yield string

    def num_bytes(self):
        """
        Return size of bitarray data, in bytes.
        """
        return len(self.data)

    def __getitem__(self, key):
        """
        Fetch value of bit at given `key` as boolean value.
        """
        if key > self.length:
            raise IndexError(f'{self.__class__.__name__} index out of range')
        index, offset = divmod(key, 8)
        return True if (self.data[index] >> offset) & 1 else False

    def __len__(self):
        """
        Return the number of bits in the array.
        """
        return self.length

    def __repr__(self):
        """
        Class name plus enough formatted data to fit on a line.
        """
        name = self.__class__.__qualname__
        return "<{}:{}>".format(name, self.__str__()[:68])

    def __setitem__(self, key, value):
        if key > self.length:
            raise IndexError(f'{self.__class__.__name__} index out of range')

        index, offset = divmod(key, 8)
        byte = self.data[index]

        value = bool(value)
        if value:
            # Set bit
            byte |= (1 << offset)
        else:
            # Clear bit
            byte &= ~(1 << offset)

        self.data[index] = byte

    def __str__(self):
        """
        Return enough data to fill a line.

        Use `iter_string()` if you need more.
        """
        parts = []
        for string in self.iter_string():
            parts.append(string)
            if len(parts) > 8:
                break
        return ''.join(parts)
