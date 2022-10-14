import unittest
from unittest import skip
from unittest.mock import patch

import pydice.dice_string.dice_string_parser as dice_parser
from pydice.dice_string.dice_parse_exceptions import DiceParseError
from pydice.dice_string.dice_parser_failures import InvalidDice, UnfinishedOperator
from pydice.dice_string.dice_string_parser import ParsedDiceString
from pydice.dice_string.operators import AddOperator, SubtractOperator, EqualToOperator, \
    GreaterThanEqualToOperator
from pydice.die import Dice, Die, FateDie
from pydice.roll_result import DiceRollResult
from pydice.roll_result_operators.counter_roll_result_decorator import CountValuesEqualToDecorator, \
    CountValuesGreaterThanDecorator, \
    CountValuesLessThanDecorator, CountValuesNotEqualToDecorator
from pydice.roll_result_operators.roll_result_decorators import AddToRollResultDecorator, \
    SubtractFromRollResultDecorator, \
    MultiplyRollResultDecorator, DivideByRollResultDecorator

dice_results = [9, 10, 6, 7, 6, 1, 2, 4, 8, 3]


class ParsedDiceStringTests(unittest.TestCase):
    def setUp(self) -> None:
        self._default_roll_result = dice_results[:1]
        self.d20 = Dice(Die(20), 1)
        self.ten_d10 = Dice(Die(10), 10)


class IsValidTests(ParsedDiceStringTests):
    def test_having_error_failure_returns_false(self):
        # Arrange
        test_parsed_dice_string = ParsedDiceString("1d20")
        test_parsed_dice_string.failures = [InvalidDice("1d20")]
        
        # Act
        result = test_parsed_dice_string.is_valid
        
        # Assert
        self.assertFalse(result)
        
    def test_having_warning_failure_returns_true(self):
        # Arrange
        test_parsed_dice_string = ParsedDiceString("1d20")
        test_parsed_dice_string.failures = [UnfinishedOperator("+6")]

        # Act
        result = test_parsed_dice_string.is_valid

        # Assert
        self.assertTrue(result)
        
    def test_having_no_failures_returns_true(self):
        # Arrange
        test_parsed_dice_string = ParsedDiceString("1d20")

        # Act
        result = test_parsed_dice_string.is_valid

        # Assert
        self.assertTrue(result)
        
    def test_having_warning_and_error_failures_returns_false(self):
        # Arrange
        test_parsed_dice_string = ParsedDiceString("1d20")
        test_parsed_dice_string.failures = [InvalidDice("1d20"), UnfinishedOperator("+5")]

        # Act
        result = test_parsed_dice_string.is_valid

        # Assert
        self.assertFalse(result)


@patch("pydice.die.random.randint", side_effect=dice_results)
class ConstructorTests(ParsedDiceStringTests):
    def test_parse_string_with_simple_roll_returns_correct_value(self, _):
        # Arrange
        expected_result = DiceRollResult(self.d20, self._default_roll_result)
        test_parser = ParsedDiceString("1d20")

        # Act
        result = test_parser.parse()

        # Assert
        self.assertEqual(expected_result, result)

    def test_parse_string_with_ten_d10_returns_correct_dice(self, _):
        # Arrange
        expected_result = DiceRollResult(self.ten_d10, dice_results)
        test_parser = ParsedDiceString("10d10")

        # Act
        result = test_parser.parse()

        # Assert
        self.assertEqual(expected_result, result)

    def test_parse_string_add_adds_decorator(self, _):
        # Arrange
        expected_result = AddToRollResultDecorator(DiceRollResult(self.d20, self._default_roll_result), 5)
        test_parser = ParsedDiceString("1d20+5")

        # Act
        result = test_parser.parse()

        # Assert
        self.assertEqual(expected_result, result)

    def test_parse_string_adding_twice_adds_decorator_twice(self, _):
        # Arrange
        expected_result = AddToRollResultDecorator(
            AddToRollResultDecorator(
                DiceRollResult(
                    self.d20,
                    self._default_roll_result
                ),
                5
            ),
            6
        )
        test_parser = ParsedDiceString("1d20+5+6")

        # Act
        result = test_parser.parse()

        # Assert
        self.assertEqual(expected_result, result)

    def test_parse_string_subtract_adds_decorator(self, _):
        # Arrange
        expected_result = SubtractFromRollResultDecorator(DiceRollResult(self.d20, self._default_roll_result), 5)
        test_parser = ParsedDiceString("1d20-5")

        # Act
        result = test_parser.parse()

        # Assert
        self.assertEqual(expected_result, result)

    def test_parse_string_multiply_adds_decorator(self, _):
        # Arrange
        expected_result = MultiplyRollResultDecorator(DiceRollResult(self.d20, self._default_roll_result), 5)
        test_parser = ParsedDiceString("1d20*5")

        # Act
        result = test_parser.parse()

        # Assert
        self.assertEqual(expected_result, result)

    def test_parse_string_divide_adds_decorator(self, _):
        # Arrange
        expected_result = DivideByRollResultDecorator(DiceRollResult(self.d20, self._default_roll_result), 5)
        test_parser = ParsedDiceString("1d20/5")

        # Act
        result = test_parser.parse()

        # Assert
        self.assertEqual(expected_result, result)

    def test_parse_equals_adds_decorator(self, _):
        # Arrange
        expected_result = CountValuesEqualToDecorator(DiceRollResult(self.d20, self._default_roll_result), 5)
        test_parser = ParsedDiceString("1d20=5")

        # Act
        result = test_parser.parse()

        # Assert
        self.assertEqual(expected_result, result)

    def test_parse_not_equals_adds_decorator(self, _):
        # Arrange
        expected_result = CountValuesNotEqualToDecorator(DiceRollResult(self.d20, self._default_roll_result), 5)
        test_parser = ParsedDiceString("1d20!=5")

        # Act
        result = test_parser.parse()

        # Assert
        self.assertEqual(expected_result, result)

    def test_parse_greater_than_adds_decorator(self, _):
        # Arrange
        expected_result = CountValuesGreaterThanDecorator(DiceRollResult(self.d20, self._default_roll_result), 5)
        test_parser = ParsedDiceString("1d20>5")

        # Act
        result = test_parser.parse()

        # Assert
        self.assertEqual(expected_result, result)

    def test_parse_greater_than_equal_adds_decorators(self, _):
        # Arrange
        expected_result = CountValuesGreaterThanDecorator(
            CountValuesEqualToDecorator(
                DiceRollResult(self.d20, self._default_roll_result), 5
            ), 5
        )
        test_parser = ParsedDiceString("1d20>=5")

        # Act
        result = test_parser.parse()

        # Assert
        self.assertEqual(expected_result, result)

    def test_parse_less_than_adds_decorator(self, _):
        # Arrange
        expected_result = CountValuesLessThanDecorator(DiceRollResult(self.d20, self._default_roll_result), 5)
        test_parser = ParsedDiceString("1d20<5")

        # Act
        result = test_parser.parse()

        # Assert
        self.assertEqual(expected_result, result)

    def test_parse_less_than_equal_adds_decorators(self, _):
        # Arrange
        expected_result = CountValuesLessThanDecorator(
            CountValuesEqualToDecorator(
                DiceRollResult(self.d20, self._default_roll_result), 5
            ), 5
        )
        test_parser = ParsedDiceString("1d20<=5")

        # Act
        result = test_parser.parse()

        # Assert
        self.assertEqual(expected_result, result)

    @skip("NotImplemented and now the code in the test is erroneous")
    def test_parse_string_two_dice_is_handled_correctly(self, _):
        # Arrange
        expected_result = None
        test_parser = ParsedDiceString("1d20+1d20")

        # Act
        result = test_parser.parse()

        # Assert
        self.assertEqual(expected_result, result)
        self.fail("Not Implemented")


class ParseTests(ParsedDiceStringTests):
    def test_parse_invalid_normal_text_raises_DiceParseError(self):
        # Assert
        with self.assertRaises(DiceParseError):
            # Act
            dice_parser.parse("hello world")

    def test_parse_dice_without_dice_size_raises_DiceParseError(self):
        # Act
        # Assert
        with self.assertRaises(DiceParseError) as ex:
            dice_parser.parse("12d")

    def test_parse_oned20_returns_correct_parser(self):
        # Act
        result = dice_parser.parse("1d20")

        # Assert
        self.assertTrue(isinstance(result, ParsedDiceString))

    def test_parse_d20_returns_correct_parser(self):
        # Act
        result = dice_parser.parse("d20")

        # Assert
        self.assertTrue(isinstance(result, ParsedDiceString))

    def test_parse_d20_parses_correct_dice(self):
        # Arrange
        expected_result = Dice(Die(20), 1)

        # Act
        result = dice_parser.parse("d20")

        # Assert
        self.assertEqual(expected_result, result._dice)

    def test_parse_d20_initialises_operators_as_empty(self):
        # Arrange
        expected_result = []

        # Act
        result = dice_parser.parse("d20")

        # Assert
        self.assertEqual(expected_result, result._operators)

    def test_parse_d20_plus_5_parses_correct_operators(self):
        # Arrange
        expected_result = [AddOperator(5)]

        # Act
        result = dice_parser.parse("d20+5")

        # Assert
        self.assertEqual(expected_result, result._operators)

    def test_parse_d20_plus_5_plus_5_parses_correct_operators(self):
        # Arrange
        expected_result = [AddOperator(5), AddOperator(5)]

        # Act
        result = dice_parser.parse("d20+5+5")

        # Assert
        self.assertEqual(expected_result, result._operators)

    def test_parse_d20_plus_5_minus_6_parses_correct_operators(self):
        # Arrange
        expected_result = [AddOperator(5), SubtractOperator(6)]

        # Act
        result = dice_parser.parse("d20+5-6")

        # Assert
        self.assertEqual(expected_result, result._operators)

    def test_parse_d20_greater_than_equal_to_parses_correct_operator(self):
        # Arrange
        expected_result = [GreaterThanEqualToOperator(5)]

        # Act
        result = dice_parser.parse("d20>=5")

        # Assert
        self.assertEqual(expected_result, result._operators)

    def test_parse_fate_dice_returns_correct_parser(self):
        # Act
        result = dice_parser.parse("dF")

        # Assert
        self.assertTrue(isinstance(result, ParsedDiceString))

    def test_parse_fate_dice_returns_fate_dice(self):
        # Act
        result = dice_parser.parse("dF")

        # Assert
        self.assertIs(FateDie, type(result._dice.die))

    def test_parse_st_returns_correct_parser(self):
        # Act
        result = dice_parser.parse("10ST10")

        # Assert
        self.assertTrue(isinstance(result, ParsedDiceString))

    def test_parse_st_returns_correct_operators(self):
        # Arrange
        expected_result = [EqualToOperator(10), GreaterThanEqualToOperator(7), AddOperator(7)]

        # Act
        result = dice_parser.parse("10st+7")

        # Assert
        self.assertEqual(expected_result, result._operators)

    def test_parse_invalid_operator_not_added_to_operators(self):
        # Arrange
        expected_results = []

        # Act
        results = dice_parser.parse("1d20never10")

        # Assert
        self.assertEqual(expected_results, results._operators)

    def test_parse_no_operator_at_end_does_not_hider_operator_creation(self):
        # Arrange
        expected_results = [AddOperator(5)]

        # Act
        results = dice_parser.parse("1d20+5ne")

        # Assert
        self.assertEqual(expected_results, results._operators)


if __name__ == '__main__':
    unittest.main()
