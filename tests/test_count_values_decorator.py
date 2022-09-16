import unittest
from unittest.mock import MagicMock

from pydice.roll_result import CountValuesDecorator, RollResult


class CountValuesDecoratorTests(unittest.TestCase):
    def setUp(self) -> None:
        self.mock_roll_result = MagicMock(spec=RollResult)
        self.mock_roll_result.die_rolls = [1, 3, 3, 3, 5]


class ResultTests(CountValuesDecoratorTests):
    def test_counts_target_number_as_expected(self):
        # Arrange
        expected_result = 3
        test_roll_result = CountValuesDecorator(self.mock_roll_result, 3)

        # Act
        result = test_roll_result.result()

        # Assert
        self.assertEqual(expected_result, result)

    def test_returns_0_if_no_number_is_target_number(self):
        # Arrange
        expected_result = 0
        test_roll_result = CountValuesDecorator(self.mock_roll_result, 6)

        # Act
        result = test_roll_result.result()

        # Assert
        self.assertEqual(expected_result, result)


if __name__ == '__main__':
    unittest.main()
