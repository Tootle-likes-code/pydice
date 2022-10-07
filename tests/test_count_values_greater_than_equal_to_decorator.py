import unittest
from unittest.mock import MagicMock

from pydice.roll_result import RollResult, CountValuesGreaterThanEqualToDecorator


class CountValueGreaterThanEqualToDecoratorTests(unittest.TestCase):
    def setUp(self) -> None:
        self.mock_roll_result = MagicMock(spec=RollResult)
        self.mock_roll_result.die_rolls = [1, 3, 3, 3, 5]


class ResultTests(CountValueGreaterThanEqualToDecoratorTests):
    def test_counts_target_number_as_expected(self):
        # Arrange
        expected_result = 4
        test_roll_result = CountValuesGreaterThanEqualToDecorator(self.mock_roll_result, 3)

        # Act
        result = test_roll_result.result()

        # Assert
        self.assertEqual(expected_result, result)

    def test_returns_0_if_no_number_is_gteq_target_number(self):
        # Arrange
        expected_result = 0
        test_roll_result = CountValuesGreaterThanEqualToDecorator(self.mock_roll_result, 6)

        # Act
        result = test_roll_result.result()

        # Assert
        self.assertEqual(expected_result, result)


if __name__ == '__main__':
    unittest.main()
