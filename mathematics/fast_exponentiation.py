


def power(base: int, exponent: int) -> int:
    """
    Recursively raise base to the power of the given exponent.
    """
    print(f"power({base}, {exponent})")
    if exponent == 0:
        return 1

    x = power(base, exponent // 2)

    if (exponent % 2) == 0:
        return x**2
    else:
        return base * x**2


if __name__ == '__main__':
    print(power(2, 1000))
    print(2**1000)
