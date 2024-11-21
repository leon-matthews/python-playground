
import argparse
import logging
from os.path import basename, dirname
import sys

from matplotlib import pyplot

from grub.data import Data
from grub.log import Log
from grub.plot import plot


class Main:
    def __init__(self, arguments):
        parser = self.make_parser()
        self.options = parser.parse_args(arguments)
        level = logging.DEBUG if self.options.verbose else logging.INFO
        logging.basicConfig(format="%(message)s", level=level)

    def make_parser(self):
        parser = argparse.ArgumentParser(
            description="Plot diet progress")

        parser.prog = self.parent_folder()
        parser.add_argument(
            'log_file', metavar='LOG_PATH',
            help="path to diet log")
        parser.add_argument('-v', '--verbose', action='store_true',
                            help='increase output verbosity')
        return parser

    def parent_folder(self):
        """
        A better name for the script than '__main__'
        """
        return basename(dirname(__file__))

    def show_plot(self, data):
        figure = pyplot.figure()
        plot(figure, data)
        pyplot.show()

    def show_status(self, data):
        total = data.get_total()
        if total <= 0.0:
            print(f"You have lost {abs(total):.1f}kg in total", end='')
        else:
            print(f"You have gained {total:.1f}kg in total", end='')

        weight_per_week = data.slope * 7
        if weight_per_week > 0:
            print(f", and are on track to gaining {weight_per_week:.1f}kg this week.")
        else:
            print(f", and are on track to losing {abs(weight_per_week):.1f}kg this week.")
        print(f"Tomorrow you have to beat {data.get_target():.1f}kg")

    def run(self):
        try:
            data = Data((row.date, row.weight) for row in Log(self.options.log_file))
            self.show_status(data)
            self.show_plot(data)
        except Exception as e:
            print(e)
            if self.options.verbose:
                raise


if __name__ == '__main__':
    main = Main(sys.argv[1:])
    sys.exit(main.run())
