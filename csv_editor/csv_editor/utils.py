
def spreadsheet_index(column):
    """
    Convert normal numeric 0-indexed column numbers to spreadsheet-style
    column index strings. eg::

        >>> spreadsheet_index(0)
        'A'
        >>> spreadsheet_index(25)
        'Z'
        >>> spreadsheet_index(26)
        'AA'

    This turns out to be harder than you first might imagine, as it is not
    a simple base-26 conversion: The letter 'A' sometimes represents a zero,
    sometimes a one - or prehaps like in ancient times, the zero has not
    been invented yet...

    For example, in a spreadsheet we count like this:
        A, B, ... Z, AA, AB

    While using normal base-10 positional notation it would be:
        1, 2, ... 9, 10, 11
    """
    # Convert to 1-index
    column = int(column) + 1
    result = []
    while column:
        # Convert remainder to letter
        remainder = column % 26
        if remainder == 0:
            remainder = 26
        letter = chr(ord('A') + remainder - 1)
        # Move to next order-of-magnitude
        column = (column - 1) // 26
        result.append(letter)

    # Convert to string, reversed for most-significant digit first
    return ''.join(result[::-1])
