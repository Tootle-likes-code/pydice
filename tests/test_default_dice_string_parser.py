import unittest
from unittest import skip
from unittest.mock import patch

from pydice.dice_string_parser import DefaultDiceStringParser
from pydice.die import Dice, Die
from pydice.operators import AddOperator, SubtractOperator, MultiplyOperator, DivideOperator, EqualToOperator, \
    GreaterThanEqualToOperator, GreaterThanOperator, LessThanOperator, LessThanEqualToOperator
from pydice.roll_result import DiceRollResult, AddToRollResultDecorator, SubtractFromRollResultDecorator, \
    MultiplyRollResultDecorator, DivideByRollResultDecorator, CountValuesEqualToDecorator, \
    CountValuesGreaterThanDecorator, CountValuesLessThanDecorator

dice_results = [9, 10, 6, 7, 6, 1, 2, 4, 8, 3]


class DefaultDiceStringParserTests(unittest.TestCase):
    def setUp(self) -> None:
        self._default_roll_result = dice_results[:1]
        self.d20 = Dice(Die(20), 1)
        self.ten_d10 = Dice(Die(10), 10)


@patch("pydice.die.random.randint", side_effect=dice_results)
class ParseTests(DefaultDiceStringParserTests):
    def test_parse_string_with_simple_roll_returns_correct_value(self, _):
        # Arrange
        expected_result = DiceRollResult(self.d20, self._default_roll_result)
        test_parser = DefaultDiceStringParser(self.d20)

        # Act
        result = test_parser.parse()

        # Assert
        self.assertEqual(expected_result, result)

    def test_parse_string_with_ten_d10_returns_correct_dice(self, _):
        # Arrange
        expected_result = DiceRollResult(self.ten_d10, dice_results)
        test_parser = DefaultDiceStringParser(self.ten_d10)

        # Act
        result = test_parser.parse()

        # Assert
        self.assertEqual(expected_result, result)

    def test_parse_string_add_adds_decorator(self, _):
        # Arrange
        expected_result = AddToRollResultDecorator(DiceRollResult(self.d20, self._default_roll_result), 5)
        test_parser = DefaultDiceStringParser(self.d20, [AddOperator(5)])

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
        test_parser = DefaultDiceStringParser(self.d20, [AddOperator(5), AddOperator(6)])

        # Act
        result = test_parser.parse()

        # Assert
        self.assertEqual(expected_result, result)

    def test_parse_string_subtract_adds_decorator(self, _):
        # Arrange
        expected_result = SubtractFromRollResultDecorator(DiceRollResult(self.d20, self._default_roll_result), 5)
        test_parser = DefaultDiceStringParser(self.d20, [SubtractOperator(5)])

        # Act
        result = test_parser.parse()

        # Assert
        self.assertEqual(expected_result, result)

    def test_parse_string_multiply_adds_decorator(self, _):
        # Arrange
        expected_result = MultiplyRollResultDecorator(DiceRollResult(self.d20, self._default_roll_result), 5)
        test_parser = DefaultDiceStringParser(self.d20, [MultiplyOperator(5)])

        # Act
        result = test_parser.parse()

        # Assert
        self.assertEqual(expected_result, result)

    def test_parse_string_divide_adds_decorator(self, _):
        # Arrange
        expected_result = DivideByRollResultDecorator(DiceRollResult(self.d20, self._default_roll_result), 5)
        test_parser = DefaultDiceStringParser(self.d20, [DivideOperator(5)])

        # Act
        result = test_parser.parse()

        # Assert
        self.assertEqual(expected_result, result)

    def test_parse_equals_adds_decorator(self, _):
        # Arrange
        expected_result = CountValuesEqualToDecorator(DiceRollResult(self.d20, self._default_roll_result), 5)
        test_parser = DefaultDiceStringParser(self.d20, [EqualToOperator(5)])

        # Act
        result = test_parser.parse()

        # Assert
        self.assertEqual(expected_result, result)

    def test_parse_greater_than_adds_decorator(self, _):
        # Arrange
        expected_result = CountValuesGreaterThanDecorator(DiceRollResult(self.d20, self._default_roll_result), 5)
        test_parser = DefaultDiceStringParser(self.d20, [GreaterThanOperator(5)])

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
        test_parser = DefaultDiceStringParser(self.d20, [GreaterThanEqualToOperator(5)])

        # Act
        result = test_parser.parse()

        # Assert
        self.assertEqual(expected_result, result)

    def test_parse_less_than_adds_decorator(self, _):
        # Arrange
        expected_result = CountValuesLessThanDecorator(DiceRollResult(self.d20, self._default_roll_result), 5)
        test_parser = DefaultDiceStringParser(self.d20, [LessThanOperator(5)])

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
        test_parser = DefaultDiceStringParser(self.d20, [LessThanEqualToOperator(5)])

        # Act
        result = test_parser.parse()

        # Assert
        self.assertEqual(expected_result, result)

    @skip("NotImplemented")
    def test_parse_string_two_dice_is_handled_correctly(self, _):
        # Arrange
        expected_result = None
        test_parser = DefaultDiceStringParser("1d20+1d20")

        # Act
        result = test_parser.parse()

        # Assert
        self.assertEqual(expected_result, result)
        self.fail("Not Implemented")


if __name__ == '__main__':
    unittest.main()
