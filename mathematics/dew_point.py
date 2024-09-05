
import math
from pprint import pprint as pp
from unittest import TestCase


def calculate_dew_point(temperature: float, relative_humidity: float) -> float:
    A = 17.62
    B = 243.12
    alpha = (
        ((A * temperature) / (B + temperature)) +
        math.log(relative_humidity/100.0)
    )
    return (B * alpha) / (A - alpha)


def calculate_humidex(temperature: float, relative_humidity: float) -> float:
    zero = 273.15
    dew_point = calculate_dew_point(temperature, relative_humidity)
    vapour_pressure = (
        6.11 * math.exp(5417.7530 * ((1/zero) - (1/(zero+dew_point))))
    )
    h = 0.5555 * (vapour_pressure - 10.0)
    humidex = (temperature) + h
    return humidex


class CalculateDewPointTest(TestCase):
    def test_calculate_dew_point(self) -> None:
        self.assertAlmostEqual(
            calculate_dew_point(25.0, 10.0), -8.77, places=2)

        self.assertAlmostEqual(
            calculate_dew_point(50.0, 90.0), 47.90, places=2)


class CalculateHumidexTest(TestCase):
    def test_calculate_humidex(self) -> None:
        calculate_humidex(27.4, 71)


if __name__ == '__main__':
    temperature = float(input("Temperature? "))
    relative_humidity = float(input("Relative humidity? "))
    print(f"Dew point: {calculate_dew_point(temperature, relative_humidity)}")
    print(f"Humidex: {calculate_humidex(temperature, relative_humidity)}")
