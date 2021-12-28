import unittest
from unittest.mock import MagicMock, Mock

from die import Dice
from roll_result import DiceRollResult


class DiceRollResultTests(unittest.TestCase):
    def setUp(self) -> None:
        self.mock_dice = MagicMock(spec=Dice)

        self.test_dice_roll_results = DiceRollResult(self.mock_dice, [4, 5])


class DieRollTests(DiceRollResultTests):
    def test_default_constructor_makes_empty_list(self):
        # Arrange
        expected_result = []
        test_dice_roll_results = DiceRollResult(self.mock_dice)

        # Act
        result = test_dice_roll_results.die_rolls

        # Assert
        self.assertEqual(expected_result, result)

    def test_returns_dice_results(self):
        # Arrange
        expected_results = [4, 5]

        # Act
        results = self.test_dice_roll_results.die_rolls

        # Assert
        self.assertEqual(expected_results, results)


class ResultsTest(DiceRollResultTests):
    def test_returns_correct_combined_result(self):
        # Arrange
        expected_result = 9

        # Act
        result = self.test_dice_roll_results.result()

        # Assert
        self.assertEqual(expected_result, result)

    def test_empty_rolls_returns_0(self):
        # Arrange
        expected_result = 0
        test_dice_roll_results = DiceRollResult(self.mock_dice)

        # Act
        result = test_dice_roll_results.result()

        # Assert
        self.assertEqual(expected_result, result)


class AddDieRollTests(DiceRollResultTests):
    def test_adding_roll_adds_to_result(self):
        # Arrange
        expected_result = [4, 5, 9]
        mock_roll_result = MagicMock()
        mock_roll_result.result = Mock(return_value=9)

        # Act
        self.test_dice_roll_results.add_die_roll(mock_roll_result)
        result = self.test_dice_roll_results.rolls

        # Assert
        self.assertEqual(expected_result, result)


class AddRollTests(DiceRollResultTests):
    def test_adding_roll_adds_to_result(self):
        # Arrange
        expected_result = [4, 5, -5]

        # Act
        self.test_dice_roll_results.add_roll(-5)
        result = self.test_dice_roll_results.rolls

        # Assert
        self.assertEqual(expected_result, result)


if __name__ == '__main__':
    unittest.main()
