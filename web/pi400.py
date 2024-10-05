#!/usr/bin/env python3
"""
Quick-and-dirty web scrape of local computer shop's newest Raspberry Pi products.
"""

from bs4 import BeautifulSoup       # type: ignore
import colorama                     # type: ignore
import os
import requests
import textwrap
from typing import List, NewType, Optional


colorama.init()
Html = NewType('Html', str)
Url = NewType('Url', str)
URL = Url(
    'https://www.pbtech.co.nz/category/computers/'
    'single-board-computers/brand-Raspberry%20Pi?o=age'
)


def deduplicate(strings: List[str]) -> List[str]:
    """
    Remove adjacent duplicates from input list.
    """
    out = []
    previous = None
    for string in strings:
        if string != previous:
            out.append(string)
            previous = string
    return out


def get(url: Url) -> Html:
    """
    Fetch the given URL.

    Args:
        url:
            URL of webpage to fetch

    Returns:
        Body of response.
    """
    response = requests.get(URL)
    return Html(response.text)


def find(html: Html) -> List[str]:
    """
    Parse the HTML and extract the names we're interested in.

    Return:
        Names of products.
    """
    soup = BeautifulSoup(html, 'html.parser')
    names = [a.text.strip() for a in
             soup.find_all('a', class_='item_line_name')]
    names = deduplicate(names)
    return names


def print_list(
    names: List[str],
    *,
    highlight: Optional[str] = None,
    limit: Optional[int] = None,
    truncate: bool = False,
    width: int = 72,
) -> None:
    """
    Print the list of given names.

    Args:
        names:
            The names to print.
        highlight:
            Optional substring to find and highlight if found.
        limit:
            Optional limit to the number of names to print.
        truncate:
            Truncate input text to fit into one line, otherwise wrapped.
        width:
            Maximum line-length.
    """
    if limit is not None:
        names = names[:limit]

    # Calculate padding
    index_width = len(str(len(names)))
    for index, name in enumerate(names, 1):
        numeral = f"{index:>{index_width}}). "
        title = numeral + name
        if truncate:
            if len(title) > (width - 3):
                title = title[:(width-3)] + '...'
        else:
            indent = ' ' * len(numeral)
            title = textwrap.fill(title, subsequent_indent=indent, width=width)

        # Highlighting
        if highlight:
            before, found, after = title.partition(highlight)
            if found:
                title = (
                    before +
                    colorama.Back.RED +
                    found +
                    colorama.Style.RESET_ALL +
                    after
                )

        # Print!
        print(title)


if __name__ == '__main__':
    html = get(URL)
    names = find(html)
    width, _ = os.get_terminal_size()
    print_list(names, highlight='400', truncate=False, width=width)
