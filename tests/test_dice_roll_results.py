import unittest
from unittest.mock import MagicMock

from pydice.die import Dice
from pydice.roll_result import DiceRollResult


class DiceRollResultTests(unittest.TestCase):
    def setUp(self) -> None:
        self.mock_dice = MagicMock(spec=Dice)
        self.mock_dice.min = 2
        self.mock_dice.max = 12
        self.mock_dice.roll.return_value = [4, 5]

        self.test_dice_roll_results = DiceRollResult(self.mock_dice, [4, 5])


class DieRollTests(DiceRollResultTests):
    def test_returns_dice_results(self):
        # Arrange
        expected_results = [4, 5]

        # Act
        results = self.test_dice_roll_results.die_rolls

        # Assert
        self.assertEqual(expected_results, results)

    def test_empty_rolls_rolls_dice(self):
        # Act
        DiceRollResult(self.mock_dice)

        # Assert
        self.mock_dice.roll.assert_called_once()

    def test_empty_rolls_updates_die_rolls(self):
        # Arrange
        expected_result = [4, 5]

        # Act
        test_dice_roll_results = DiceRollResult(self.mock_dice)

        # Assert
        self.assertEqual(expected_result, test_dice_roll_results.die_rolls)


class ResultsTest(DiceRollResultTests):
    def test_returns_correct_combined_result(self):
        # Arrange
        expected_result = 9

        # Act
        result = self.test_dice_roll_results.result()

        # Assert
        self.assertEqual(expected_result, result)


class AddDieRollTests(DiceRollResultTests):
    def test_adding_roll_adds_to_result(self):
        # Arrange
        expected_result = [4, 5, 3]

        # Act
        self.test_dice_roll_results.add_die_roll(3)
        result = self.test_dice_roll_results._rolls

        # Assert
        self.assertEqual(expected_result, result)

    def test_adding_roll_less_than_min_raises_Value_Error(self):
        # Arrange
        expected_args = ('Roll must be less than min and greater than max. Dice Min: 2, Dice Max: 12, '
                         'value to add: -50',)

        # Act
        with self.assertRaises(ValueError) as ex:
            self.test_dice_roll_results.add_die_roll(-50)

        # Assert
        self.assertEqual(expected_args, ex.exception.args)

    def test_adding_roll_more_than_max_raises_Value_Error(self):
        # Arrange
        expected_args = ('Roll must be less than min and greater than max. Dice Min: 2, Dice Max: 12, '
                         'value to add: 50',)

        # Act
        with self.assertRaises(ValueError) as ex:
            self.test_dice_roll_results.add_die_roll(50)

        # Assert
        self.assertEqual(expected_args, ex.exception.args)

    def test_adding_roll_equal_to_min_adds_correctly(self):
        # Arrange
        expected_result = [4, 5, 2]

        # Act
        self.test_dice_roll_results.add_die_roll(2)
        result = self.test_dice_roll_results.die_rolls

        # Assert
        self.assertEqual(expected_result, result)

    def test_adding_roll_equal_to_max_adds_correctly(self):
        # Arrange
        expected_result = [4, 5, 12]

        # Act
        self.test_dice_roll_results.add_die_roll(12)
        result = self.test_dice_roll_results.die_rolls

        # Assert
        self.assertEqual(expected_result, result)


if __name__ == '__main__':
    unittest.main()
