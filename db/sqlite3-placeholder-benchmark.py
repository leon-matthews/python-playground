#! /usr/bin/env python3

"""
Compare performance of SQLite placeholder styles.

An SQL statement may use one of two kinds of placeholders: question marks
(qmark style) or named placeholders (named style), as below.

    INSERT INTO people VALUES (?, ?, ?, ?);
    INSERT INTO people VALUES (:first_name, :last_name, :born, :died);

The question this experiment answers is what is the price we pay for the
safety and convenience of the latter syntax.

See:
    https://docs.python.org/3/library/sqlite3.html#sqlite3-placeholders
"""

import datetime
from functools import wraps
import gc
from os import PathLike
from pathlib import Path
from pprint import pprint as pp
import random
import sqlite3
import textwrap
import time
from typing import Dict, Iterable, List, Tuple, TypeAlias, Union


DataQMark: TypeAlias = Tuple[str, str, int, int]
DataNamed: TypeAlias = Dict[str, Union[int, str]]


NAMES_FOLDER = Path(__file__).parent.parent / 'data' / 'names'


def benchmark(function):
    @wraps(function)
    def wrapper(self, *args, **kwargs):
        gcold = gc.isenabled()
        gc.disable()
        start = time.perf_counter()
        try:
            retval = function(self, *args, **kwargs)
        finally:
            if gcold:
                gc.enable()
        elapsed = time.perf_counter() - start
        print(f"{function.__name__}() => {elapsed}")
        return retval
    return wrapper


def load_lines(file_name: str, encoding: str = 'utf-8') -> List[str]:
    """
    Load lines from given text file into list.

    Blank lines and lines begining with '#' are skipped.

    Args:
        path:
            Path to existing files.
        encoding:
            Encoding of text file.

    Returns:
        A list of all of the valid lines in the file.
    """
    lines = []
    path = NAMES_FOLDER / file_name
    with open(path, 'rt', encoding=encoding) as fp:
        for line in fp:
            line = line.strip()
            if not line:
                continue
            if not line.startswith('#'):
                lines.append(line)
    return lines


class PlaceHolderBenchmark:
    def __init__(self):
        self.connection = sqlite3.connect(":memory:")
        self.create_table()
        self.first_names = load_lines('given-female.txt')
        self.first_names.extend(load_lines('given-male.txt'))
        self.last_names = load_lines('surnames.txt')

    def build_data(
        self,
        count: int,
        *,
        named: bool = False,
    ) -> Iterable[Union[DataQMark, DataNamed]]:
        """
        Build random people data for benchmarking.

        Either a 4-tuple, or a dictionary of data.
        """
        now = datetime.date.today().year
        for _ in range(count):
            first_name = random.choice(self.first_names)
            last_name = random.choice(self.last_names)
            born = now - int(random.random() * 88)
            died = born + int(random.random() * 88)
            if died > now:
                died = None

            if named:
                yield {
                    'first_name': first_name,
                    'last_name': last_name,
                    'born': born,
                    'died': died,
                }
            else:
                yield (first_name, last_name, born, died)

    def create_table(self):
        query = """
            CREATE TABLE IF NOT EXISTS people(
                first_name  TEXT NOT NULL,
                last_name   TEXT NOT NULL,
                born        INTEGER NOT NULL,
                died        INTEGER
            );
        """
        query = textwrap.dedent(query).strip()
        self.connection.execute(query)

    @benchmark
    def insert_many_dicts(self, data):
        with self.connection:
            self.connection.executemany(
                "INSERT INTO people VALUES (:first_name, :last_name, :born, :died);",
                data,
            )

    @benchmark
    def insert_many_tuples(self, data):
        with self.connection:
            self.connection.executemany(
                "INSERT INTO people VALUES (?, ?, ?, ?);", data,
            )

    @benchmark
    def insert_many_tuples_into_named(self, data):
        with self.connection:
            self.connection.executemany(
                "INSERT INTO people VALUES (:first_name, :last_name, :born, :died);",
                data,
            )


if __name__ == '__main__':
    benchmark = PlaceHolderBenchmark()
    COUNT = 10_000_000

    # Insert dictionaries of data using named placeholders
    data = list(benchmark.build_data(COUNT, named=True))
    benchmark.insert_many_dicts(data)
    del data

    # Insert tuples of data using 'qmark style'
    data = list(benchmark.build_data(COUNT))
    benchmark.insert_many_tuples(data)
    del data
