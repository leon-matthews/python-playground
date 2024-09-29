
import re
import shutil
import textwrap


TERMINAL_WIDTH, _ = shutil.get_terminal_size()


def wrap_command(command, *, indent='    ', suffix=' \\', width=TERMINAL_WIDTH):
    """
    Wrap long command onto multiple lines.

    Args:
        command: String to wrap
        indent: Prepend this to every line *after* the first. Defaults to
            four spaces.
        suffix: Add this to the end of every line *except* the last.
            Defaults to a space then backslash.
        width: The maximum allowable width allowed. If not given, the
            current terminal width will be used.
    """
    # Adjust width
    width -= (len(indent) + len(suffix))

    # Easy?
    if len(command) < width:
        return command

    # Break on chained commands
    parts = re.split(r"(\s&&\s)", command)
    if len(parts) == 1:
        groups = parts
    else:
        groups = []
        for line, separator in itertools.zip_longest(parts[::2], parts[1::2]):
            groups.append(line + (separator if separator else ''))

    # Break lines within parts
    lines = []
    for group in groups:
        if len(group) < width:
            lines.append(group)
        else:
            lines.extend(textwrap.wrap(
                group,
                break_on_hyphens=False,
                replace_whitespace=False,
                width=width))

    # Add suffixes and indents
    num_lines = len(lines)
    is_first = True
    is_last = False
    output = []
    for num, line in enumerate(lines, 1):
        if num == num_lines:
            is_last = True
        if not is_first:
            line = indent + line
        if not is_last:
            line = line + suffix
        is_first = False
        output.append(line)

    return '\n'.join(output)
