
from collections import OrderedDict
import csv
import os
import sys

from .utils import spreadsheet_index


class CsvTransform:
    def __init__(self, options):
        self.allow_overwrite = options.force
        self.encoding_input = options.encoding_input
        self.encoding_output = options.encoding_output
        self.limit = options.limit
        self.path_in = options.path_in
        self.path_out = options.path_out
        self.skip_header = options.skip_header

    def run(self):
        self.check_paths()
        self.process_file()

    def check_paths(self):
        """
        Catch common path errors.
        """
        message = None
        if self.path_out and os.path.exists(self.path_out):

            # Don't overwrite existing files by default
            if not self.allow_overwrite:
                message = "Output file already exists. Use '--force' to overwrite"

            # Try not to nuke our input file!
            if os.path.samefile(self.path_in, self.path_out):
                message = 'Output and input are the same file.'

        if message:
            raise RuntimeError(message)

    def convert_row(self, row):
        """
        Convert row into dictionary for easier manipulation, eg.

        ['apple', 'banana', 'carrot']

        converts to a dictionary with spreadsheet-style column headings.

        {
            'A': 'apple',
            'B': 'banana',
            'C': 'carrot'
        }
        """
        record = OrderedDict()
        for index, cell in enumerate(row):
            index = spreadsheet_index(index)
            record[index] = cell
        return record

    def process_file(self):
        """
        Iterate over every CSV record in the given file.

        path
            Path to input file.
        """
        num_processed = 0
        with self._open_input() as fin, self._open_output() as fout:
            reader = csv.reader(fin)
            writer = csv.writer(fout)
            for index, row in enumerate(reader, 1):
                if index == 1 and self.skip_header:
                    continue

                record = self.convert_row(row)
                self.process_record(record)
                num_processed += 1

                writer.writerow(record.values())

                if self.limit and num_processed >= self.limit:
                    break

    def process_record(self, record):
        """
        Return record after make any modifications you wish here.
        """
        raise NotImplementedError()

    def _open_input(self):
        """
        Return opened output file.
        """
        return open(self.path_in, 'rt', newline='', encoding=self.encoding_input)

    def _open_output(self):
        """
        Return opened output file, or stdout if no output file given.
        """
        if self.path_out:
            return open(self.path_out, 'wt', newline='', encoding=self.encoding_output)
        else:
            return sys.stdout
