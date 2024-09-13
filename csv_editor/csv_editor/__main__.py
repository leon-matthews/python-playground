#!/usr/bin/env python3

"""
Create copy of Shopify database export with some fields edited.
"""

import argparse
import re
import sys

from .transform import CsvTransform


def create_parser():
    """
    Create argparse-based command-line parser.
    """
    parser = argparse.ArgumentParser(description='Shopify Data Modification.')

    parser.add_argument(
        'path_in',
        metavar='FILE_IN',
        type=str,
        help="path to input CSV file")

    parser.add_argument(
        'path_out',
        metavar='FILE_OUT',
        nargs='?',
        type=str,
        help="path to output CSV file (optional)")

    parser.add_argument(
        '--encoding-input',
        metavar='',
        default='utf-8',
        type=str,
        help="Text encoding of input CSV file (default utf-8)")

    parser.add_argument(
        '--encoding-output',
        default='utf-8',
        metavar='',
        type=str,
        help="Text encoding of output file (default utf-8)")

    parser.add_argument(
        '-f', '--force',
        action='store_true',
        help="Allow overwriting of output file")

    parser.add_argument(
        '-H', '--skip-header',
        action='store_true',
        help="Do not process the first record")

    parser.add_argument(
        '-l', '--limit',
        metavar='N',
        type=int,
        help="Stop processing after N rows")

    return parser


class ShopifySearchReplace(CsvTransform):
    regex_start = re.compile(r"<h5>Active Ingredients</h5>")
    regex_end = re.compile(r"<h4>")

    def process_record(self, record):
        """
        Replace part of column C with full text of column K.
        """
        c = record['C']
        k = record['K']
        parts = []

        # Find start
        match = self.regex_start.search(c)
        start = 0
        if match:
            start = match.start()
            parts.append(c[:start])
            parts.append(k)
        else:
            parts.append(c)

        # Find end
        match = self.regex_end.search(c, start)
        if match:
            parts.append(c[match.start():])

        # Save changes
        record['C'] = ''.join(parts)
        return record


def main(args):
    parser = create_parser()
    options = parser.parse_args(args)
    processor = ShopifySearchReplace(options)
    processor.run()


if __name__ == '__main__':
    sys.exit(main(sys.argv[1:]))
