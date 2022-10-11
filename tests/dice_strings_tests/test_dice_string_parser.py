import unittest

from pydice.dice_string import dice_string_parser as dice_parser
from pydice.dice_string.dice_string_parser import DefaultDiceStringParser
from pydice.die import Dice, Die, FateDie
from pydice.dice_string.operators import AddOperator, SubtractOperator, GreaterThanEqualToOperator, EqualToOperator


class DiceStringParserTests(unittest.TestCase):
    pass


class CreateTests(DiceStringParserTests):
    def test_create_invalid_normal_text_returns_none(self):
        # Act
        result = dice_parser.create("hello world")

        # Assert
        self.assertIsNone(result)

    def test_create_dice_without_dice_size_returns_none(self):
        # Act
        result = dice_parser.create("12d")

        # Assert
        self.assertIsNone(result)

    def test_create_oned20_returns_correct_parser(self):
        # Act
        result = dice_parser.create("1d20")

        # Assert
        self.assertTrue(isinstance(result, DefaultDiceStringParser))

    def test_create_d20_returns_correct_parser(self):
        # Act
        result = dice_parser.create("d20")

        # Assert
        self.assertTrue(isinstance(result, DefaultDiceStringParser))

    def test_create_d20_parses_correct_dice(self):
        # Arrange
        expected_result = Dice(Die(20), 1)

        # Act
        result = dice_parser.create("d20")

        # Assert
        self.assertEqual(expected_result, result.dice)

    def test_create_d20_initialises_operators_as_empty(self):
        # Arrange
        expected_result = []

        # Act
        result = dice_parser.create("d20")

        # Assert
        self.assertEqual(expected_result, result._operators)

    def test_create_d20_plus_5_parses_correct_operators(self):
        # Arrange
        expected_result = [AddOperator(5)]

        # Act
        result = dice_parser.create("d20+5")

        # Assert
        self.assertEqual(expected_result, result._operators)

    def test_create_d20_plus_5_plus_5_parses_correct_operators(self):
        # Arrange
        expected_result = [AddOperator(5), AddOperator(5)]

        # Act
        result = dice_parser.create("d20+5+5")

        # Assert
        self.assertEqual(expected_result, result._operators)

    def test_create_d20_plus_5_minus_6_parses_correct_operators(self):
        # Arrange
        expected_result = [AddOperator(5), SubtractOperator(6)]

        # Act
        result = dice_parser.create("d20+5-6")

        # Assert
        self.assertEqual(expected_result, result._operators)

    def test_create_d20_greater_than_equal_to_parses_correct_operator(self):
        # Arrange
        expected_result = [GreaterThanEqualToOperator(5)]

        # Act
        result = dice_parser.create("d20>=5")

        # Assert
        self.assertEqual(expected_result, result._operators)

    def test_create_fate_dice_returns_correct_parser(self):
        # Act
        result = dice_parser.create("dF")

        # Assert
        self.assertTrue(isinstance(result, DefaultDiceStringParser))

    def test_create_fate_dice_returns_fate_dice(self):
        # Act
        result = dice_parser.create("dF")

        # Assert
        self.assertIs(FateDie, type(result.dice.die))

    def test_create_st_returns_correct_parser(self):
        # Act
        result = dice_parser.create("10ST10")

        # Assert
        self.assertTrue(isinstance(result, DefaultDiceStringParser))

    def test_create_st_returns_correct_operators(self):
        # Arrange
        expected_result = [EqualToOperator(10), GreaterThanEqualToOperator(7), AddOperator(7)]

        # Act
        result = dice_parser.create("10st+7")

        # Assert
        self.assertEqual(expected_result, result._operators)

    def test_create_invalid_operator_not_added_to_operators(self):
        # Arrange
        expected_results = []

        # Act
        results = dice_parser.create("1d20never10")

        # Assert
        self.assertEqual(expected_results, results._operators)

    def test_create_no_operator_at_end_does_not_hider_operator_creation(self):
        # Arrange
        expected_results = [AddOperator(5)]

        # Act
        results = dice_parser.create("1d20+5ne")

        # Assert
        self.assertEqual(expected_results, results._operators)


if __name__ == '__main__':
    unittest.main()
