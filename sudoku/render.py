


def draw_ascii(board):
    """
    Draw board in plain ole' ASCII.

    For example::

        +-------+-------+-------+
        | 6 8 . | 4 . 3 | . 5 . |
        | 4 . 2 | . 5 . | 3 6 8 |
        | 5 9 3 | 6 7 8 | . . 4 |
        +-------+-------+-------+
        | . 1 7 | 2 8 6 | 9 4 5 |
        | 8 . 9 | 5 . 4 | 2 . 7 |
        | 2 5 4 | 3 9 7 | 8 1 . |
        +-------+-------+-------+
        | 7 . . | 8 3 1 | 5 9 2 |
        | 9 3 5 | . 6 . | 4 . 1 |
        | . 2 . | 9 . 5 | . 7 3 |
        +-------+-------+-------+

    """
    lines = []
    hr = '+' + (('-' * (2 * board.box_width + 1)) + '+') * board.box_width
    a = '|' + ('{}'.join([' '] * (board.box_width + 1)) + '|') * board.box_width

    lines.append(hr)
    numbers = [str(n) if n else '.' for n in board.data]
    for row in range(board.width):
        start = row * board.width
        out = numbers[start:start + board.width]
        if row and (row % board.box_width == 0):
            lines.append(hr)
        lines.append(a.format(*out))
    lines.append(hr)
    return "\n".join(lines)


def draw_unicode(board):
    """
    Draw board using Unicode box-drawing characters.

    https://en.wikipedia.org/wiki/Box-drawing_character

    For example::

        ╔═══╤═══╤═══╦═══╤═══╤═══╦═══╤═══╤═══╗
        ║ 6 │ 8 │   ║ 4 │   │ 3 ║   │ 5 │   ║
        ╟───┼───┼───╫───┼───┼───╫───┼───┼───╢
        ║ 4 │   │ 2 ║   │ 5 │   ║ 3 │ 6 │ 8 ║
        ╟───┼───┼───╫───┼───┼───╫───┼───┼───╢
        ║ 5 │ 9 │ 3 ║ 6 │ 7 │ 8 ║   │   │ 4 ║
        ╠═══╪═══╪═══╬═══╪═══╪═══╬═══╪═══╪═══╣
        ║   │ 1 │ 7 ║ 2 │ 8 │ 6 ║ 9 │ 4 │ 5 ║
        ╟───┼───┼───╫───┼───┼───╫───┼───┼───╢
        ║ 8 │   │ 9 ║ 5 │   │ 4 ║ 2 │   │ 7 ║
        ╟───┼───┼───╫───┼───┼───╫───┼───┼───╢
        ║ 2 │ 5 │ 4 ║ 3 │ 9 │ 7 ║ 8 │ 1 │   ║
        ╠═══╪═══╪═══╬═══╪═══╪═══╬═══╪═══╪═══╣
        ║ 7 │   │   ║ 8 │ 3 │ 1 ║ 5 │ 9 │ 2 ║
        ╟───┼───┼───╫───┼───┼───╫───┼───┼───╢
        ║ 9 │ 3 │ 5 ║   │ 6 │   ║ 4 │   │ 1 ║
        ╟───┼───┼───╫───┼───┼───╫───┼───┼───╢
        ║   │ 2 │   ║ 9 │   │ 5 ║   │ 7 │ 3 ║
        ╚═══╧═══╧═══╩═══╧═══╧═══╩═══╧═══╧═══╝

    """
    def build_row(fill, chars, sqrt):
        parts = []
        add = parts.append
        add(chars[0])
        for i in range(sqrt):
            if i:
                add(chars[2])
            for j in range(sqrt):
                if j:
                    add(chars[1])
                add(fill)
        add(chars[-1])
        return ''.join(parts)

    lines = []
    top = build_row('═══', '╔╤╦╗', board.box_width)
    fat = build_row('═══', '╠╪╬╣', board.box_width)
    thin = build_row('───', '╟┼╫╢', board.box_width)
    content = build_row(' {} ', '║│║║', board.box_width)
    bottom = build_row('═══', '╚╧╩╝', board.box_width)

    lines.append(top)
    numbers = [str(n) if n else ' ' for n in board.data]
    for row in range(board.width):
        if row:
            lines.append(fat if (row % board.box_width == 0) else thin)
        start = row * board.width
        out = numbers[start:start + board.width]
        lines.append(content.format(*out))

    lines.append(bottom)
    return "\n".join(lines)
