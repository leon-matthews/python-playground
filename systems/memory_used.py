"""
Determine RAM used by process using only standard library.

See:
    Alternative, cross-platform 3rd-party libary.
    https://psutil.readthedocs.io/en/latest/
"""

import resource


def bytes_used() -> int:
    """
    Bytes of RAM currently used by script.

    Uses the standard library resource module, which is Linux/Unix only.

    Note that the given is the current script process' MAXRSS. Determining how
    much memory a process is actually using is complicated on a modern OS with
    virtual memory. I prefer the `smem` command-line tool to get a more accurate
    picture.

    See:
        Details about the getrusage() function from standard C library.
        https://manpages.debian.org/bookworm/manpages-dev/getrusage.2.en.html

    Returns:
        Raw number of bytes used.
    """
    fields = resource.getrusage(resource.RUSAGE_SELF)
    # On Linux `ru_maxrss` is given in kilobytes.
    num_bytes = fields.ru_maxrss * 1024
    return num_bytes


def megabytes(num_bytes: int) -> str:
    """
    Format given number of bytes to human-friendly string.
    """
    megabytes = num_bytes / 1024 / 1024
    return f"{megabytes:.1f}MB"


if __name__ == '__main__':
    used = bytes_used()
    print(megabytes(used))
