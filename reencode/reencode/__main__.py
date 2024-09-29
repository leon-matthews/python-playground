#!/usr/bin/env python3

import argparse
import builtins
import logging
from pathlib import Path
from pprint import pprint as pp
import sys

from .ffmpeg import FFMpeg
from .ffprobe import FFProbe


builtins.pp = pp
logger = logging.getLogger(__name__)


def argparse_existing_file(string):
    """
    An `argparse` type to convert string to a `Path` object.

    Raises `argparse.ArgumentTypeError` if path does not exist.
    """
    path = Path(string).expanduser().resolve()
    error = None
    if not path.exists():
        error = f"File does not exist: {path}"
    if not path.is_file():
        error = f"Path is not a file: {path}"

    if error is not None:
        raise argparse.ArgumentTypeError(error)
    return path


def argparse_existing_folder(string):
    """
    An `argparse` type to convert string to a `Path` object.

    Raises `argparse.ArgumentTypeError` if path does not exist.
    """
    path = Path(string).expanduser().resolve()
    error = None
    if not path.exists():
        error = f"Folder does not exist: {path}"
    if not path.is_dir():
        error = f"Path is not a folder: {path}"

    if error is not None:
        raise argparse.ArgumentTypeError(error)
    return path


def configure_logging():
    logging.basicConfig(
        format="%(levelname)s %(name)s %(message)s",
        level=logging.DEBUG)


def parse_args(arguments):
    parser = argparse.ArgumentParser(description='Re-encode flabby video files')
    parser.add_argument(
        'folder',
        metavar='FOLDER',
        type=argparse_existing_folder,
        help="Folder containing media files")
    parser.add_argument(
        '-n', '--dry-run',
        action='store_true',
        help="Only show actions to perform, do not ")
    options = parser.parse_args()
    return options


def main(options):
    """
    Main function.

    Args:
        options (argparse.Namespace)
    """
    for input_path in options.folder.glob('*.mp4'):
        ffprobe = FFProbe(input_path)
        info = ffprobe.run()
        pp(vars(info))
        output_path = Path('output') / input_path.name
        encoder = FFMpeg(input_path, output_path)
        encoder.run(dry_run=options.dry_run)
        print()


if __name__ == '__main__':
    configure_logging()
    options = parse_args(sys.argv)
    sys.exit(main(options))
