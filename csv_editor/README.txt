
=============================
Shopify Export Search/Replace
=============================

:Author: Leon Matthews
:Contact: http://DigitalAdvisor.nz/
:date:  14 June 2016

This is a small script to create a modified copy of an input CSV file::

    Shopify Data Modification.

    positional arguments:
      FILE_IN              path to input CSV file
      FILE_OUT             path to output CSV file (optional)

    optional arguments:
      -h, --help           show this help message and exit
      --encoding ENCODING  Text encoding of input file (output is always utf-8)
      -f, --force          Allow overwriting of output file
      -H, --skip-header    Do not process the first record
      -l N, --limit N      Stop processing after N row


Replacement Logic
=================

For every row, part of column `C` may be replaced with the entire contents of
column `K`, per the following steps. (Every possibility is tested in the
files `test.csv`, and `test.replaced.csv`).

Examine column `C`:

* If the heading `<h5>Active Ingredients</h5>` is not found, leave column as-is.
* If found, replace that heading and the text following it with the contents
  of column `K`, up until...
* The end of the column's text or the string `<h4>`, whichever comes first.


Requirements
============

This is a Python 3 script, to be run from the command-line. It uses only
standard-library modules, no 3rd party code is required.
