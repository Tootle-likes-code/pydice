import unittest
from unittest.mock import MagicMock

from pydice.die import Die
from pydice.roll_result import RollResult
from pydice.roll_result_operators.roll_result_decorators import ExplodeDiceForTargetDecorator


class ExplodeDiceForTargetDecoratorTests(unittest.TestCase):
    def setUp(self) -> None:
        self.mock_die = MagicMock(spec=Die)
        self.mock_die.roll.return_value = 4

        self.mock_result = MagicMock(spec=RollResult)
        self.mock_result.die_rolls = [3, 4, 6]
        self.mock_result.rolled_die = self.mock_die

        self.test_exploding_roll_result = ExplodeDiceForTargetDecorator(self.mock_result, 6)


class ResultTests(ExplodeDiceForTargetDecoratorTests):
    def test_dice_hitting_target_number_causes_exploding_value(self):
        # Arrange
        expected_results = 17

        # Act
        results = self.test_exploding_roll_result.result()

        # Assert
        self.assertEqual(expected_results, results)

    def test_calling_result_again_does_not_change_result(self):
        # Act
        result1 = self.test_exploding_roll_result.result()
        result2 = self.test_exploding_roll_result.result()

        # Assert
        self.assertEqual(result1, result2)

    def test_another_exploding_value_causes_the_result_to_explode_again(self):
        # Arrange
        # [3,4,6,6,1]
        expected_result = 20
        self.mock_die.roll.side_effect = [6, 1]

        # Act
        result = self.test_exploding_roll_result.result()

        # Assert
        self.assertEqual(expected_result, result)


if __name__ == '__main__':
    unittest.main()
