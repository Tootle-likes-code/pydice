import unittest
from unittest.mock import MagicMock, PropertyMock

from pydice.die import Die
from pydice.roll_result import RollResult
from pydice.roll_result_operators.roll_result_decorators import ExplodeDiceForTargetDecorator


class ExplodeDiceForTargetDecoratorTests(unittest.TestCase):
    def setUp(self) -> None:
        self.mock_die = MagicMock(spec=Die)
        self.mock_die.roll.side_effect = [[6], [1]]

        self.mock_result = MagicMock(spec=RollResult)
        self.mock_result.die_rolls = [3, 4, 6]
        self.mock_result.rolled_die = self.mock_die

        self.test_none_exploding_roll_result = ExplodeDiceForTargetDecorator(self.mock_result, 1)
        self.test_exploding_roll_result = ExplodeDiceForTargetDecorator(self.mock_result, 6)


class ConstructorTests(ExplodeDiceForTargetDecoratorTests):
    def setUp(self) -> None:
        super().setUp()
        self.mock_die = MagicMock(spec=Die)
        self.test_result = MagicMock(spec=RollResult)
        self.mock_die_results = PropertyMock(return_value=[3, 4, 6])
        type(self.test_result).die_rolls = self.mock_die_results

    def test_calls_given_roll_result_die_rolls(self):
        # Act
        ExplodeDiceForTargetDecorator(self.test_result, 1)

        # Assert
        self.mock_die_results.assert_called_once()


class DieRollTests(ExplodeDiceForTargetDecoratorTests):
    def test_new_rolls_are_in_die_roll(self):
        # Arrange
        expected_results = [3, 4, 6, 6, 1]

        # Act
        results = self.test_exploding_roll_result.die_rolls

        # Assert
        self.assertEqual(expected_results, results)


class ResultTests(ExplodeDiceForTargetDecoratorTests):
    def test_double_exploding_returns_correct_value(self):
        # Arrange
        expected_results = 20

        # Act
        results = self.test_exploding_roll_result.result

        # Assert
        self.assertEqual(expected_results, results)

    def test_no_dice_exploding_return_new_sum(self):
        # Arrange
        expected_results = 13

        # Act
        results = self.test_none_exploding_roll_result.result

        # Assert
        self.assertEqual(expected_results, results)

    def test_calling_result_again_does_not_change_result(self):
        # Act
        result1 = self.test_exploding_roll_result.result
        result2 = self.test_exploding_roll_result.result

        # Assert
        self.assertEqual(result1, result2)


if __name__ == '__main__':
    unittest.main()
