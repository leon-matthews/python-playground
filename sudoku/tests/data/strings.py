
import textwrap


ascii_grid = textwrap.dedent("""

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

""").strip()


unicode_grid = textwrap.dedent("""

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

""").strip()