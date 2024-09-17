
import collections
import csv
import logging
import re


logger = logging.getLogger(__name__)


class NamedTupleReader:
    """
    Read CSV file, using first heading row as namedtuple keys.

    Columns with no heading in the first row are skipped.

    The first key in the named tuple is 'row_index' and corresponds to the
    line number or spreadsheet index of the source file.
    """
    clean_heading_regex = re.compile(r'[^a-z0-9_]+')

    def __init__(self, csvfile):
        """
        Initialiser.

        Args:
            csvfile (file):
               Open file-like object to CSV file.

        """
        self.reader = csv.reader(csvfile)
        self.headings = self.read_heading()
        self.namedtuple = self.create_namedtuple(self.headings)

    def __iter__(self):
        for index, data in enumerate(self.reader, 2):
            row = self.create_tuple(index, data)
            yield row

    def create_namedtuple(self, headings):
        """
        Create a namedtuple type.

        Args:
            headings (list):
                List of heading strings

        Return namedtuple type.
        """
        namedtuple = collections.namedtuple('Row', ['line'] + headings)
        return namedtuple

    def read_heading(self):
        """
        Read the heading from the CSV file to create named tuple.

        Args:
            reader (csv.reader):
                CSV reader object.

        Return list of heading strings.
        """
        # Read heading, parse and clean names
        headings = next(self.reader)
        headings = [self.clean_heading(heading) for heading in headings]
        return headings

    def clean_heading(self, heading):
        """
        Convert heading into a valid Python identifier
        """
        cleaned = heading.lower()
        cleaned = self.clean_heading_regex.sub('_', cleaned)
        cleaned = cleaned.strip('_')
        return cleaned

    def create_tuple(self, line, data):
        """
        Populate given namedtemplate class, taking care to properly
        skip the empty columns.

        Args:
            line (int):
                Line number of row.
            data (list):
                List of fields from CSV file.

        Returns (namedtuple):
            Row as a named tuple.
        """
        data = [datum.strip() for datum in data]
        try:
            row = self.namedtuple(line, *data)
        except TypeError:
            message = f"Line {line:,}: Expected {self.headings!r}, found {data!r}"
            raise TypeError(message) from None
        return row
