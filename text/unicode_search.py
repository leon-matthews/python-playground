#!/usr/bin/env python3

"""
Quick-and-dirty search of Python's built-in Unicode Character Database.

For example:

    $ ./unicode_search.py 'cat face'
    decimal   hex   chr                     name
    -------   ---   ---   ----------------------------------------
     128049  1F431   🐱   Cat Face
     128568  1F638   😸   Grinning Cat Face With Smiling Eyes
     128569  1F639   😹   Cat Face With Tears Of Joy
     128570  1F63A   😺   Smiling Cat Face With Open Mouth
     128571  1F63B   😻   Smiling Cat Face With Heart-Shaped Eyes
     128572  1F63C   😼   Cat Face With Wry Smile
     128573  1F63D   😽   Kissing Cat Face With Closed Eyes
     128574  1F63E   😾   Pouting Cat Face
     128575  1F63F   😿   Crying Cat Face
     128576  1F640   🙀   Weary Cat Face

There is a lot to see in there! Try 'arrow', 'box', 'digit three', or
even 'hieroglyph'...
"""

import sys
import unicodedata


def print_unicode_table(words: list[str]) -> None:
    """
    Search and print unicode database in one pass.
    """
    # Heading
    print(f"decimal   hex   chr  {'name':^40}")
    print(f"-------   ---   ---  {'-':-<40}")

    words = [word.casefold() for word in words]
    for code in range(0, sys.maxunicode):
        c = chr(code)
        name = unicodedata.name(c, '*** unknown ***')
        if all([word in name.casefold() for word in words]):
            print(f"{code:7}  {code:5X}  {code:^3c}  {name}")


if __name__ == '__main__':
    if len(sys.argv) == 1:
        print('usage: {0} [string]'.format(sys.argv[0]) )
        sys.exit(1)

    words =  sys.argv[1:]
    print_unicode_table(words)
