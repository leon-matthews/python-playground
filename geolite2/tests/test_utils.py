
from ipaddress import IPv4Address, IPv4Network

from unittest import TestCase

from geolite2.utils import calculate_range


class CalculateRangeTest(TestCase):
    def test_calculate_range(self):
        network = IPv4Network('192.168.0.0/24')
        first, last = calculate_range(network)

        # Raw integers
        self.assertEqual(first, 3232235520)
        self.assertEqual(last, 3232235775)

        # Convert back to IP addresses
        first = IPv4Address(first)
        last = IPv4Address(last)
        self.assertEqual(first, IPv4Address('192.168.0.0'))
        self.assertEqual(last, IPv4Address('192.168.0.255'))
