"""
Learn how Lempel-Ziv tokenisation works.

We're not compressing data here, we're only experimenting with how to break
input characters into an optimal token stream.

TODO:
    * Implement look_back() function.
"""

from dataclasses import dataclass


@dataclass
class Token:
    """
    Encapsulate token data.
    """
    offset: int
    length: int
    literal: str|None = None

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}{self}"

    def __str__(self) -> str:
        if self.literal is None:
            string = f"({self.offset}, {self.length})"
        else:
            string = f"({self.offset}, {self.length}, {self.literal!r})"
        return string


def look_back(needle: str, haystack: str, max_length: int|None = None) -> int|None:
    """
    Search backwards for needle in haystack.

    Returns the offset from the end of the first matching character::

        >>> look_back('a', 'Bubba')
        1
        >>> look_back('ub', 'Bubba')
        4
        >>> look_back('Z', 'Bubba')
        None

    You can extract the matching substring by inverting the sign::

        >>> 'Bubba'[-1]
        'a'
        >>> 'Bubba'[-4: -len('ub')]
        'ub'

    Args:
        needle:
            String to search for.
        haystack:
            String to search in.
        max_length:
            Optionally give up searching after this many characters.

    Returns:
        Offset from end of string, or none if needle not found.
    """
    return None


def tokenise(string) -> list[Token]:
    """
    Convert string into list of tokens.

    Args:
        string:
            Input to break into tokens.

    Returns:
    """
    # Empty string
    tokens: list[Token] = []
    if not string:
        return tokens

    # First character
    current = 0
    word = string[current]
    tokens.append(Token(current, len(word), word))
    current += 1
    length = 1

    def longest_match(current) -> tuple[int, str]:
        return (0, "")
        # ~ while current < len(string):
            # ~ length = 1
            # ~ word = string[current:current+length]




            # ~ while (found := string.find(word, 0, current)) != -1:
                # ~ length += 1

                # ~ current += 1

    tokens.append(Token(current, length, word))

    return tokens


def untokenise(tokens: list[Token]) -> str:
    """
    Recreate original string from tokens.

    Args:
        tokens:
            Tokens produced from `tokenise()` function.

    Returns:
        Plain string.
    """
    string = ''
    if not tokens:
        return string

    for token in tokens:
        string = f"{string}{token.literal}"

    return string
