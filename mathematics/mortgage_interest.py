#!/usr/bin/env python3
"""
Calculate how much your mortage payments are affected by rate changes.

You can use it to calculate how much interest you're being charged::

    $ ./mortgage_interest.py 750_000 4.79%
    Interest only on $750,000 at 4.79% is $3,066.40 per month.

And how that will change when the bank changs your rate::

    $ ./mortgage_interest.py 750_000 4.79% 6.79%
    Interest only on $750,000 at 4.79% is $3,066.40 per month.
    Changing to 6.79% will cost $4,391 = $1,324 MORE per month.

Note that the calculation is just the interest component of your monthly
payments. You will have to pay some principal at some point, and that amount
will change based on your term and how far through it you are.

I'm interest only in the change to my monthly payments. In the example above
I can see that whatever I'm having to pay now, once the new interest rate
kicks in I'll be out $1,324 more per month. Ouch!
"""

import argparse
import sys


def compound_interest(
    principal: float,
    rate: float,
    years: int,
    times_per_year: int = 365,
) -> float:
    """
    Calculate the compound interest accrued.

    Args:
        principal:
            Starting value of mortgage or investment.
        rate:
            Interest rate as a percentage, eg. 5.6
        years:
            Number of years to calculate for.
        times_per_year:
            Number of times per year that interest is calculated. Defaults
            to 365 for daily interest calculation.

    Returns:
        Total value after interest applied for given years.
    """
    rate /= 100
    body = 1 + (rate / times_per_year)                      # (1 + r/n)
    exponent = times_per_year * years                       # nt
    interest = principal * pow(body, exponent)              # P(1 + r/n)**nt
    return interest


def monthly_interest(principal: float, rate: float) -> float:
    """
    Calculate the amount of interest accrued per month.
    """
    annual = compound_interest(principal, rate, 1) - principal
    return annual / 12


def percentage(string: str) -> float:
    """
    Be friendly with the percentage values we accept.

    Args:
        string:
            Interest rate with possible trailing percentage symbol.

    Returns:
        Floating-point value
    """
    percentage = float(string.rstrip('%').strip())
    return percentage


def parse_args(arguments: list[str]) -> argparse.Namespace:
    """
    Parse command-line arguments to produce set of options to give to `main()`.
    """
    description = "Calculate monthly mortgage payments"
    parser = argparse.ArgumentParser(description=description)
    parser.add_argument(
        'principal',
        metavar='PRINCIPAL',
        type=float,
        help='Currrent principal remaining',
    )
    parser.add_argument(
        'rate_current',
        metavar='INTEREST',
        type=percentage,
        help='Current interest rate',
    )
    parser.add_argument(
        'rate_next',
        metavar='NEW RATE',
        nargs='?',
        type=percentage,
        help='Optional interest rate to compare',
    )
    return parser.parse_args()


def main(options: argparse.Namespace) -> int:
    # Current interest accrued
    interest_current = monthly_interest(options.principal, options.rate_current)
    print(
        f"Interest only on ${options.principal:,.0f} "
        f"at {options.rate_current}% is ${interest_current:,.2f} per month. "
    )

    # Calculate difference?
    if options.rate_next:
        interest_next = monthly_interest(options.principal, options.rate_next)
        delta = interest_current - interest_next
        adjective = 'LESS' if delta > 0 else 'MORE'

        print(
            f"Changing to {options.rate_next}% will cost ${interest_next:,.0f}"
            f" = ${abs(delta):,.0f} {adjective} per month."
        )

    return 0


if __name__ == '__main__':
    options = parse_args(sys.argv[1:])
    sys.exit(main(options))
