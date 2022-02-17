import unittest
from unittest.mock import patch

from pydice.die import Dice, Die, DicePool


class DicePoolTests(unittest.TestCase):
    def setUp(self) -> None:
        self.d6 = Die(6)
        self.d8 = Die(8)
        self.dice_2d6 = Dice(die=self.d6, number_of_dice=2)
        self.dice_3d8 = Dice(die=self.d8, number_of_dice=3)
        self.test_dice_pool = DicePool(self.d6, self.dice_2d6, self.dice_3d8)


class InitTests(DicePoolTests):
    def test_single_rollable_creates_with_rollable(self):
        # Arrange
        expected_result = [self.dice_2d6]

        # Act
        dice_pool = DicePool(self.dice_2d6)

        # Assert
        self.assertEqual(expected_result, dice_pool._rollables)

    def test_multiple_rollable_of_varying_types_creates_from_rollable(self):
        # Arrange
        expected_result = [self.dice_2d6, self.dice_3d8, self.d8]

        # Act
        dice_pool = DicePool(self.dice_2d6, self.dice_3d8, self.d8)

        # Assert
        self.assertEqual(expected_result, dice_pool._rollables)

    def test_non_rollable_is_ignored(self):
        # Arrange
        expected_result = [self.dice_2d6, self.dice_3d8]

        # Act
        dice_pool = DicePool(self.dice_2d6, "hello world", self.dice_3d8)

        # Assert
        self.assertEqual(expected_result, dice_pool._rollables)


@patch("pydice.die.random.randint", side_effect=range(1, 8))
class RollTests(DicePoolTests):
    def test_roll_gets_expected_value(self, _):
        # Arrange
        expected_result = [1, 2, 3, 4, 5, 6]

        # Act
        result = self.test_dice_pool.roll()

        # Assert
        self.assertEqual(expected_result, result)


class MinTests(DicePoolTests):
    def test_minimum_is_total_of_all_rollables(self):
        # Arrange
        expected_result = 6

        # Act
        result = self.test_dice_pool.min

        # Assert
        self.assertEqual(expected_result, result)


class MaxTests(DicePoolTests):
    def test_maximum_is_total_of_all_rollables(self):
        # Arrange
        expected_result = 42

        # Act
        result = self.test_dice_pool.max

        # Assert
        self.assertEqual(expected_result, result)


if __name__ == '__main__':
    unittest.main()
