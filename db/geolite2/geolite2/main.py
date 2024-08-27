"""
Command-line interface.
"""

import argparse
import ipaddress
import logging
from pprint import pprint as pp

from . import db
from .csv import NamedTupleReader
from . import utils


class Main:
    """
    Configurable callable.
    """
    def __init__(self, arguments):
        parser = self.make_parser()
        self.options = parser.parse_args(arguments)
        self.configure_logging(self.options.verbose)

    def __call__(self):
        reader = NamedTupleReader(self.options.csv)
        for row in reader:
            pp(row)
            break
        return 0

    def configure_logging(self, verbose):
        level = logging.DEBUG if verbose else logging.INFO
        logging.basicConfig(force=True, format="%(message)s", level=level)
        logging.getLogger('sqlalchemy').setLevel(logging.WARNING)
        if verbose:
            logging.getLogger('sqlalchemy.engine').setLevel(logging.INFO)

    def make_parser(self):
        parser = argparse.ArgumentParser(
            description="Import GeoLite2 data into an SQL database")
        parser.add_argument('-v', '--verbose', action='store_true',
                            help='increase output verbosity')
        parser.add_argument(
            'csv',
            metavar='FILE',
            type=argparse.FileType('r', encoding='UTF-8'),
            help='path to CSV file')
        return parser
