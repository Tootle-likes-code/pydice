import unittest
from unittest.mock import patch, call

from pydice.dice_string import dice_string_parser
from pydice.dice_string.dice_parser_failures import InvalidDice, UnfinishedOperator
from pydice.dice_string.parsed_dice_string import ParsedDiceString
from pydice.die import Dice, Die
from pydice.roll_result import DiceRollResult

dice_results = [9, 10, 6, 7, 6, 1, 2, 4, 8, 3]


class ParsedDiceStringTests(unittest.TestCase):
    def setUp(self) -> None:
        self._default_roll_result = dice_results[:1]
        self.d20 = Dice(Die(20), 1)
        self.ten_d10 = Dice(Die(10), 10)
        self.dice_result = DiceRollResult(self.d20, [17])


class IsValidTests(ParsedDiceStringTests):
    def test_having_error_failure_returns_false(self):
        # Arrange
        test_parsed_dice_string = ParsedDiceString("1d20", [InvalidDice("1d20")], None)

        # Act
        result = test_parsed_dice_string.is_valid

        # Assert
        self.assertFalse(result)

    def test_having_warning_failure_returns_true(self):
        # Arrange
        test_parsed_dice_string = ParsedDiceString("1d20", [UnfinishedOperator("+6")], self.dice_result)

        # Act
        result = test_parsed_dice_string.is_valid

        # Assert
        self.assertTrue(result)

    def test_having_no_failures_but_no_roll_result_returns_false(self):
        # Arrange
        test_parsed_dice_string = ParsedDiceString("1d20", [], None)

        # Act
        result = test_parsed_dice_string.is_valid

        # Assert
        self.assertFalse(result)

    def test_having_no_failures_and_roll_result_returns_true(self):
        # Arrange
        test_parsed_dice_string = ParsedDiceString("1d20", [], self.dice_result)

        # Act
        result = test_parsed_dice_string.is_valid

        # Assert
        self.assertTrue(result)

    def test_having_warning_and_error_failures_and_roll_result_returns_false(self):
        # Arrange
        test_parsed_dice_string = ParsedDiceString("1d20", [InvalidDice("1d20"), UnfinishedOperator("+5")],
                                                   self.dice_result)

        # Act
        result = test_parsed_dice_string.is_valid

        # Assert
        self.assertFalse(result)


if __name__ == '__main__':
    unittest.main()
