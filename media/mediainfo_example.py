#!/usr/bin/env python3
"""
Print brief metadata about media files found in the current folder.

Playing around with using mediainfo via the `pymediainfo` library.

See:
    https://pymediainfo.readthedocs.io/
"""

from pathlib import Path
from pprint import pprint as pp
import sys
from typing import Any, Iterable


from pymediainfo import MediaInfo, Track


def find_files(root: Path) -> Iterable[Path]:
    """
    Yield the plain files found under given root.
    """
    for path in root.iterdir():
        # Regular files only
        if not path.is_file():
            continue

        # Skip hidden files
        if path.name.startswith('.'):
            continue

        yield path


def get_name(general: Track) -> str:
    name = general.commercial_name
    if name is None:
        name = general.file_extension
    return name


def mediainfo(path: Path):
    info = MediaInfo.parse(path)
    general = info.general_tracks[0]
    if general is None:
        pp((general, path))
    else:
        pp(get_name(general))


def main(root: Path) -> None:
    if root.is_file():
        info = mediainfo(root)
    else:
        for path in find_files(root):
            info = mediainfo(path)


if __name__ == '__main__':
    if len(sys.argv) == 1:
        root = Path.cwd()
    elif len(sys.argv) == 2:
        root = Path(sys.argv[1]).expanduser().resolve()
    else:
        print(f"usage: {sys.argv[0]} [FOLDER]", file=sys.stderr)

    main(root)
