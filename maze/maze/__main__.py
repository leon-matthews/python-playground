
import argparse
import logging
from pprint import pprint as pp
import sys

from maze import Maze


def main(width, height):
    maze = Maze(width, height)
    maze.fill()
    pp(maze)


def parse_arguments(args):
    parser = argparse.ArgumentParser(description='Draw a maze, using recursive backtracker')
    parser.add_argument('--height', default=50, type=int)
    parser.add_argument('--width', default=50, type=int)
    return parser.parse_args()


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO, format="%(message)s")
    options = parse_arguments(sys.argv)
    sys.exit(main(options.width, options.height))
