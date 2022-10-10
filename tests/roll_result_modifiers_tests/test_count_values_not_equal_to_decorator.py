import unittest
from unittest.mock import MagicMock

from pydice.roll_result import RollResult
from pydice.roll_result_modifiers.counter_roll_result_decorator import CountValuesEqualToDecorator, CountValuesNotEqualToDecorator


class CountValuesNotEqualToDecoratorTests(unittest.TestCase):
    def setUp(self) -> None:
        self.mock_roll_result = MagicMock(spec=RollResult)
        self.mock_roll_result.die_rolls = [1, 3, 3, 3, 5]


class ResultTests(CountValuesNotEqualToDecoratorTests):
    def test_counts_target_number_as_expected(self):
        # Arrange
        expected_result = 2
        test_roll_result = CountValuesNotEqualToDecorator(self.mock_roll_result, 3)

        # Act
        result = test_roll_result.result()

        # Assert
        self.assertEqual(expected_result, result)

    def test_returns_0_if_no_number_is_target_number(self):
        # Arrange
        expected_result = 0
        self.mock_roll_result.die_rolls = [6, 6, 6, 6, 6]
        test_roll_result = CountValuesNotEqualToDecorator(self.mock_roll_result, 6)

        # Act
        result = test_roll_result.result()

        # Assert
        self.assertEqual(expected_result, result)

    def test_result_if_prior_roll_result_is_an_CountRollResult_add_to_previous_result(self):
        # Arrange
        expected_result = 5
        test_roll_result = CountValuesNotEqualToDecorator(CountValuesEqualToDecorator(self.mock_roll_result, 3), 3)

        # Act
        result = test_roll_result.result()

        # Assert
        self.assertEqual(expected_result, result)


if __name__ == '__main__':
    unittest.main()
