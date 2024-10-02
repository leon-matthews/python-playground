
import csv
from dataclasses import dataclass
import datetime
from os.path import abspath, basename, isfile

from .utils import skip_comments


@dataclass
class Record:
    def __post_init__(self):
        self.date = datetime.date.fromisoformat(self.date)
        self.weight = float(self.weight)

    date: datetime.date
    weight: float
    note: str


class Log:
    """
    Interface to weight-loss log file.
    """
    def __init__(self, path, encoding='utf-8'):
        self.encoding = encoding
        self.path = abspath(path)
        if not isfile(self.path):
            message = f"Log file not found: {self.path}"
            raise FileNotFoundError(message)

    def __iter__(self):
        with open(self.path, mode='rt', newline='', encoding=self.encoding) as fp:
            reader = csv.reader(filter(skip_comments, fp))
            for row in reader:
                datum = Record(*row)
                yield datum

    def __repr__(self):
        name = self.__class__.__name__
        return f"{name}('{basename(self.path)}', encoding='{self.encoding}')"
