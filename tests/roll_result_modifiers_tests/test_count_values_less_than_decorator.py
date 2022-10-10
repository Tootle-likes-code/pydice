import unittest
from unittest.mock import MagicMock, PropertyMock

from pydice.roll_result import RollResult
from pydice.roll_result_operators.counter_roll_result_decorator import CountValuesEqualToDecorator, \
    CountValuesLessThanDecorator, CounterRollResultDecorator


class CountValuesLessThanDecoratorTests(unittest.TestCase):
    def setUp(self) -> None:
        self.mock_roll_result = MagicMock(spec=RollResult)
        self.mock_roll_result.die_rolls = [1, 3, 3, 3, 5]


class ConstructorTests(CountValuesLessThanDecoratorTests):
    def setUp(self) -> None:
        self.mock_roll_result = MagicMock(spec=CounterRollResultDecorator)
        self.mock_die_rolls = PropertyMock()
        self.mock_result = PropertyMock()

        type(self.mock_roll_result).die_rolls = self.mock_die_rolls
        type(self.mock_roll_result).result = self.mock_result

    def test_given_roll_result_die_rolls_is_called(self):
        # Act
        CountValuesLessThanDecorator(self.mock_roll_result, 3)

        # Assert
        self.mock_die_rolls.assert_called_once()

    def test_given_roll_result_is_counter_roll_result_decorator_calls_result(self):
        # Act
        CountValuesLessThanDecorator(self.mock_roll_result, 3)

        # Assert
        self.mock_result.assert_called_once()


class ResultTests(CountValuesLessThanDecoratorTests):
    def test_counts_target_number_as_expected(self):
        # Arrange
        expected_result = 1
        test_roll_result = CountValuesLessThanDecorator(self.mock_roll_result, 3)

        # Act
        result = test_roll_result.result

        # Assert
        self.assertEqual(expected_result, result)

    def test_returns_0_if_no_number_is_lt_target_number(self):
        # Arrange
        expected_result = 0
        test_roll_result = CountValuesLessThanDecorator(self.mock_roll_result, 1)

        # Act
        result = test_roll_result.result

        # Assert
        self.assertEqual(expected_result, result)

    def test_if_prior_result_is_a_counter_decorator_adds_count_to_total(self):
        # Arrange
        expected_result = 4
        test_roll_result = CountValuesLessThanDecorator(
            CountValuesEqualToDecorator(self.mock_roll_result, 3), 2)

        # Act
        result = test_roll_result.result

        # Assert
        self.assertEqual(expected_result, result)


if __name__ == '__main__':
    unittest.main()
