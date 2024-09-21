#!/usr/bin/env python3

import collections
import csv

import wddx




ENCODING = 'latin-1'


# Location
Row = collections.namedtuple('Row', 'site name wddx cat1 cat2 cat3 valid id')


def rows():
    with open('dump.csv', 'rt', encoding=ENCODING) as fin:
        reader = csv.reader(fin)
        for row in reader:
            yield Row(*row)





from pprint import pprint

if __name__ == '__main__':
    # Deserialise WDDX
    for row in rows():
        data = wddx.loads(row.wddx)
        print(data[0]['category'])


    # Write CSV file
    #~ with open('output.csv', 'wt', encoding='utf-8') as fout:
        #~ writer = csv.writer(fout)
        #~ for row in rows():
            #~ row = (row.id, row.valid, row.name.strip(), row.cat1, row.cat2, row.cat3)
            #~ writer.writerow(row)
