import unittest
from unittest.mock import MagicMock

from pydice.roll_result import CountValuesEqualToDecorator, RollResult


class CountValuesEqualToDecoratorTests(unittest.TestCase):
    def setUp(self) -> None:
        self.mock_roll_result = MagicMock(spec=RollResult)
        self.mock_roll_result.die_rolls = [1, 3, 3, 3, 5]


class ResultTests(CountValuesEqualToDecoratorTests):
    def test_counts_target_number_as_expected(self):
        # Arrange
        expected_result = 3
        test_roll_result = CountValuesEqualToDecorator(self.mock_roll_result, 3)

        # Act
        result = test_roll_result.result()

        # Assert
        self.assertEqual(expected_result, result)

    def test_returns_0_if_no_number_is_target_number(self):
        # Arrange
        expected_result = 0
        test_roll_result = CountValuesEqualToDecorator(self.mock_roll_result, 6)

        # Act
        result = test_roll_result.result()

        # Assert
        self.assertEqual(expected_result, result)
        
    def test_result_if_prior_roll_result_is_an_CountRollResult_add_to_previous_result(self):
        # Arrange
        expected_result = 4
        test_roll_result = CountValuesEqualToDecorator(CountValuesEqualToDecorator(self.mock_roll_result, 3), 1)
        
        # Act
        result = test_roll_result.result()
        
        # Assert
        self.assertEqual(expected_result, result)


if __name__ == '__main__':
    unittest.main()
