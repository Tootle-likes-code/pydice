import unittest
from unittest.mock import MagicMock, PropertyMock

from pydice.die import Dice, Die
from pydice.roll_result import RollResult, DiceRollResult
from pydice.roll_result_operators.counter_roll_result_decorator import CountValuesEqualToDecorator, \
    CounterRollResultDecorator


class CountValuesEqualToDecoratorTests(unittest.TestCase):
    def setUp(self) -> None:
        self.die_results = [1, 3, 3, 3, 5]
        self.mock_roll_result = MagicMock(spec=RollResult)
        self.mock_roll_result.die_rolls = self.die_results


class ConstructorTests(CountValuesEqualToDecoratorTests):
    def setUp(self) -> None:
        self.mock_roll_result = MagicMock(spec=CounterRollResultDecorator)
        self.mock_die_rolls = PropertyMock()
        self.mock_result = PropertyMock()

        type(self.mock_roll_result).die_rolls = self.mock_die_rolls
        type(self.mock_roll_result).result = self.mock_result

    def test_given_roll_result_die_rolls_is_called(self):
        # Act
        CountValuesEqualToDecorator(self.mock_roll_result, 3)

        # Assert
        self.mock_die_rolls.assert_called_once()

    def test_given_roll_result_is_counter_roll_result_decorator_calls_result(self):
        # Act
        CountValuesEqualToDecorator(self.mock_roll_result, 3)

        # Assert
        self.mock_result.assert_called_once()


class ResultTests(CountValuesEqualToDecoratorTests):
    def test_counts_target_number_as_expected(self):
        # Arrange
        expected_result = 3
        roll_result = DiceRollResult(Dice(Die(6), 5), self.die_results)
        test_roll_result = CountValuesEqualToDecorator(roll_result, 3)

        # Act
        result = test_roll_result.result

        # Assert
        self.assertEqual(expected_result, result)

    def test_returns_0_if_no_number_is_target_number(self):
        # Arrange
        expected_result = 0
        test_roll_result = CountValuesEqualToDecorator(self.mock_roll_result, 6)

        # Act
        result = test_roll_result.result

        # Assert
        self.assertEqual(expected_result, result)


if __name__ == '__main__':
    unittest.main()
