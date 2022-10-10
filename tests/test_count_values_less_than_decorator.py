import unittest
from unittest.mock import MagicMock

from pydice.roll_result import RollResult
from pydice.counter_roll_result_decorator import CountValuesEqualToDecorator, CountValuesLessThanDecorator


class CountValuesLessThanDecoratorTests(unittest.TestCase):
    def setUp(self) -> None:
        self.mock_roll_result = MagicMock(spec=RollResult)
        self.mock_roll_result.die_rolls = [1, 3, 3, 3, 5]


class ResultTests(CountValuesLessThanDecoratorTests):
    def test_counts_target_number_as_expected(self):
        # Arrange
        expected_result = 1
        test_roll_result = CountValuesLessThanDecorator(self.mock_roll_result, 3)

        # Act
        result = test_roll_result.result()

        # Assert
        self.assertEqual(expected_result, result)

    def test_returns_0_if_no_number_is_lt_target_number(self):
        # Arrange
        expected_result = 0
        test_roll_result = CountValuesLessThanDecorator(self.mock_roll_result, 1)

        # Act
        result = test_roll_result.result()

        # Assert
        self.assertEqual(expected_result, result)

    def test_if_prior_result_is_a_counter_decorator_adds_count_to_total(self):
        # Arrange
        expected_result = 4
        test_roll_result = CountValuesLessThanDecorator(
            CountValuesEqualToDecorator(self.mock_roll_result, 3), 2)

        # Act
        result = test_roll_result.result()

        # Assert
        self.assertEqual(expected_result, result)


if __name__ == '__main__':
    unittest.main()
