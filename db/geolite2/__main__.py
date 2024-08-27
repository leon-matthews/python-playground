
import sys

from geolite2 import main


if __name__ == '__main__':
    program = main.Main(sys.argv[1:])
    sys.exit(program())
