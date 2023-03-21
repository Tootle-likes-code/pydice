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


class DiceTests(DiceRollResultTests):
    def test_can_get(self):
        # Assert
        self.assertEqual(self.test_dice_roll_results._dice, self.mock_dice)

    def test_cannot_be_set(self):
        # Assert
        with self.assertRaises(AttributeError) as ex:
            # Act
            self.test_dice_roll_results._dice = 123


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
        result = self.test_dice_roll_results.result

        # Assert
        self.assertEqual(expected_result, result)


if __name__ == '__main__':
    unittest.main()
