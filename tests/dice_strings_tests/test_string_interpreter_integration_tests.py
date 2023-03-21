import unittest
from unittest import skip
from unittest.mock import patch

from pydice.dice_string.dice_parser_failures import UnfinishedOperator
from pydice.dice_string.dice_string_interpreter import interpret
from pydice.dice_string.parsed_dice_string import ParsedDiceString
from pydice.die import Dice, Die, FateDie
from pydice.roll_result import DiceRollResult
from pydice.roll_result_operators.counter_roll_result_decorator import CountValuesEqualToDecorator, \
    CountValuesGreaterThanDecorator, \
    CountValuesLessThanDecorator, CountValuesNotEqualToDecorator
from pydice.roll_result_operators.drop_dice_roll_result_decorators import DropHighestDecorator, DropLowestDecorator
from pydice.roll_result_operators.roll_result_decorators import AddToRollResultDecorator, \
    SubtractFromRollResultDecorator, \
    MultiplyRollResultDecorator, DivideByRollResultDecorator, ExplodeDiceForTargetDecorator

dice_results = [9, 10, 6, 7, 6, 1, 2, 4, 8, 3]
default_fate_result = [-1, 1, 0, 0]
default_story_teller_dice_results = [
    3, 7, 2, 5, 7,
    6, 9, 4, 1, 2,
    5, 1, 8, 10, 4
]


class StringInterpreterTests(unittest.TestCase):
    pass


@patch("pydice.die.random.randint", side_effect=dice_results)
class InterpretTests(StringInterpreterTests):
    def setUp(self) -> None:
        self._default_roll_result = dice_results[:1]
        self.d20 = Dice(Die(20), 1)
        self.five_d20 = Dice(Die(20), 5)
        self.ten_d10 = Dice(Die(10), 10)

    def test_interpret_with_simple_roll_returns_correct_value(self, _):
        # Arrange
        expected_result = ParsedDiceString("1d20", [], DiceRollResult(self.d20, [9]))

        # Act
        result = interpret("1d20")

        # Assert
        self.assertEqual(expected_result, result)

    def test_interpret_with_numberless_d20_returns_correct_dice(self, _):
        # Arrange
        expected_result = ParsedDiceString("d20", [], DiceRollResult(self.d20, [9]))

        # Act
        result = interpret("d20")

        # Assert
        self.assertEqual(expected_result, result)

    def test_interpret_with_ten_d10_returns_correct_dice(self, _):
        # Arrange
        expected_result = ParsedDiceString(
            "10d10", [], DiceRollResult(self.ten_d10, [9, 10, 6, 7, 6, 1, 2, 4, 8, 3])
        )

        # Act
        result = interpret("10d10")

        # Assert
        self.assertEqual(expected_result, result)

    def test_interpret_d_case_does_not_matter(self, _):
        # Arrange
        expected_result = ParsedDiceString("1D20", [], DiceRollResult(self.d20, [9]))

        # Act
        result = interpret("1D20")

        # Assert
        self.assertEqual(expected_result, result)

    def test_interpret_add_adds_decorator(self, _):
        # Arrange
        expected_result = ParsedDiceString(
            "1d20+5",
            [],
            AddToRollResultDecorator(DiceRollResult(self.d20, [9]), 5)
        )

        # Act
        result = interpret("1d20+5")

        # Assert
        self.assertEqual(expected_result, result)

    def test_interpret_adding_twice_adds_decorator_twice(self, _):
        # Arrange
        expected_result = ParsedDiceString(
            "1d20+5+6",
            [],
            AddToRollResultDecorator(
                AddToRollResultDecorator(DiceRollResult(self.d20, [9]), 5),
                6)
        )

        # Act
        result = interpret("1d20+5+6")

        # Assert
        self.assertEqual(expected_result, result)

    def test_interpret_subtract_adds_decorator(self, _):
        # Arrange
        expected_result = ParsedDiceString(
            "1d20-5",
            [],
            SubtractFromRollResultDecorator(DiceRollResult(self.d20, [9]), 5)
        )

        # Act
        result = interpret("1d20-5")

        # Assert
        self.assertEqual(expected_result, result)

    def test_interpret_multiply_adds_decorator(self, _):
        # Arrange
        expected_result = ParsedDiceString(
            "1d20*5",
            [],
            MultiplyRollResultDecorator(DiceRollResult(self.d20, [9]), 5)
        )

        # Act
        result = interpret("1d20*5")

        # Assert
        self.assertEqual(expected_result, result)

    def test_interpret_divide_adds_decorator(self, _):
        # Arrange
        expected_result = ParsedDiceString(
            "1d20/5",
            [],
            DivideByRollResultDecorator(DiceRollResult(self.d20, [9]), 5)
        )

        # Act
        result = interpret("1d20/5")

        # Assert
        self.assertEqual(expected_result, result)

    def test_interpret_equal_to_adds_decorator(self, _):
        # Arrange
        expected_result = ParsedDiceString(
            "1d20=9",
            [],
            CountValuesEqualToDecorator(DiceRollResult(self.d20, [9]), 9)
        )

        # Act
        result = interpret("1d20=9")

        # Assert
        self.assertEqual(expected_result, result)

    def test_interpret_greater_than_adds_decorator(self, _):
        # Arrange
        expected_result = ParsedDiceString(
            "1d20>9",
            [],
            CountValuesGreaterThanDecorator(DiceRollResult(self.d20, self._default_roll_result), 9))

        # Act
        result = interpret("1d20>9")

        # Assert
        self.assertEqual(expected_result, result)

    def test_interpret_greater_than_equal_to_adds_greater_than_and_equal_to_decorator(self, _):
        # Arrange
        expected_result = ParsedDiceString(
            "1d20>=15",
            [],
            CountValuesGreaterThanDecorator(
                CountValuesEqualToDecorator(
                    DiceRollResult(self.d20, self._default_roll_result), 15
                ), 15
            )
        )

        # Act
        result = interpret("1d20>=15")

        # Assert
        self.assertEqual(expected_result, result)

    def test_interpret_less_than_adds_decorator(self, _):
        # Arrange
        expected_result = ParsedDiceString(
            "1d20<9",
            [],
            CountValuesLessThanDecorator(DiceRollResult(self.d20, self._default_roll_result), 9)
        )

        # Act
        result = interpret("1d20<9")

        # Assert
        self.assertEqual(expected_result, result)

    def test_interpret_less_than_equal_to_adds_decorator(self, _):
        # Arrange
        expected_result = ParsedDiceString(
            "1d20<=9",
            [],
            CountValuesLessThanDecorator(
                CountValuesEqualToDecorator(
                    DiceRollResult(self.d20, self._default_roll_result), 9
                ), 9
            )
        )

        # Act
        result = interpret("1d20<=9")

        # Assert
        self.assertEqual(expected_result, result)

    def test_interpret_not_equal_to_adds_decorator(self, _):
        # Arrange
        expected_result = ParsedDiceString(
            "1d20!=9",
            [],
            CountValuesNotEqualToDecorator(DiceRollResult(self.d20, self._default_roll_result), 9)
        )

        # Act
        result = interpret("1d20!=9")

        # Assert
        self.assertEqual(expected_result, result)

    def test_interpret_not_equal_to_alt_adds_decorator(self, _):
        # Arrange
        expected_result = ParsedDiceString(
            "1d20=/=9",
            [],
            CountValuesNotEqualToDecorator(DiceRollResult(self.d20, self._default_roll_result), 9)
        )

        # Act
        result = interpret("1d20=/=9")

        # Assert
        self.assertEqual(expected_result, result)

    def test_interpret_explodes_adds_decorator(self, mock_die_rolls):
        # Arrange
        mock_die_rolls.side_effect = [4] + default_story_teller_dice_results
        expected_result = ParsedDiceString(
            "14d10e10",
            [],
            ExplodeDiceForTargetDecorator(DiceRollResult(Dice(Die(10), 14),
                                                         default_story_teller_dice_results[:-1]), 10)
        )

        # Act
        result = interpret("14d10e10")

        # Assert
        self.assertEqual(expected_result, result)

    @skip("NotImplemented")
    def test_interpret_two_dice_is_handled_correctly(self, _):
        # Arrange
        expected_result = None

        # Act
        result = interpret("1d20+1d20")

        # Assert
        self.assertEqual(expected_result, result)
        self.fail("Not Implemented")

    def test_interpret_unfinished_operators_returns_operator_failure(self, _):
        # Arrange
        expected_result = ParsedDiceString(
            "1d20+5e",
            [UnfinishedOperator("e")],
            AddToRollResultDecorator(DiceRollResult(self.d20, [9]), 5)
        )

        # Act
        result = interpret("1d20+5e")

        # Assert
        self.assertEqual(expected_result, result)

    def test_interpret_drop_highest_operator_adds_decorator(self, _):
        # Arrange
        expected_result = ParsedDiceString(
            "5d20dh3",
            [],
            DropHighestDecorator(DiceRollResult(self.five_d20, dice_results[:5]), 3)
        )

        # Act
        result = interpret("5d20dh3")

        # Assert
        self.assertEqual(expected_result, result)

    def test_interpret_drop_lowest_operator_adds_decorator(self, _):
        # Arrange
        expected_result = ParsedDiceString(
            "5d20dl3",
            [],
            DropLowestDecorator(DiceRollResult(self.five_d20, dice_results[:5]), 3)
        )

        # Act
        result = interpret("5d20dl3")

        # Assert
        self.assertEqual(expected_result, result)


@patch("pydice.die.random.randint", side_effect=default_fate_result)
class InterpretWithFateTests(StringInterpreterTests):
    def setUp(self) -> None:
        self.fate_dice = Dice(FateDie(), 4)

    def test_interpret_fate_die_rolls_four_dice(self, _):
        # Arrange
        expected_result = ParsedDiceString("df", [], DiceRollResult(self.fate_dice, default_fate_result))

        # Act
        result = interpret("df")

        # Assert
        self.assertEqual(expected_result, result)

    def test_interpret_fate_die_with_add_is_added(self, _):
        # Arrange
        expected_result = ParsedDiceString(
            "df+2",
            [],
            AddToRollResultDecorator(DiceRollResult(self.fate_dice, default_fate_result), 2)
        )

        # Act
        result = interpret("df+2")

        # Assert
        self.assertEqual(expected_result, result)

    def test_interpret_fate_die_case_insensitive(self, _):
        # Arrange
        expected_result = ParsedDiceString("DF", [], DiceRollResult(self.fate_dice, default_fate_result))

        # Act
        result = interpret("DF")

        # Assert
        self.assertEqual(expected_result, result)


@patch("pydice.die.random.randint", side_effect=default_story_teller_dice_results)
class StorytellerInterpretTest(StringInterpreterTests):
    def setUp(self) -> None:
        self._test_dice = Dice(Die(10), 15)

    def test_storyteller_dice_are_correctly_interpreted(self, _):
        # Arrange
        expected_result = ParsedDiceString(
            "15st",
            [],
            CountValuesGreaterThanDecorator(
                CountValuesEqualToDecorator(
                    CountValuesEqualToDecorator(
                        DiceRollResult(self._test_dice, default_story_teller_dice_results), 10),
                    7),
                7
            )
        )

        # Act
        result = interpret("15st")

        # Assert
        self.assertEqual(expected_result, result)

    def test_storyteller_dice_adding_successes_correctly_interpreted(self, _):
        # Arrange
        expected_result = ParsedDiceString(
            "15st+7",
            [],
            AddToRollResultDecorator(
                CountValuesGreaterThanDecorator(
                    CountValuesEqualToDecorator(
                        CountValuesEqualToDecorator(
                            DiceRollResult(self._test_dice, default_story_teller_dice_results), 10),
                        7),
                    7),
                7
            )
        )

        # Act
        result = interpret("15st+7")

        # Assert
        self.assertEqual(expected_result, result)

    def test_storyteller_case_insensitive(self, _):
        # Arrange
        expected_result = ParsedDiceString(
            "15ST",
            [],
            CountValuesGreaterThanDecorator(
                CountValuesEqualToDecorator(
                    CountValuesEqualToDecorator(
                        DiceRollResult(self._test_dice, default_story_teller_dice_results), 10),
                    7),
                7
            )
        )

        # Act
        result = interpret("15ST")

        # Assert
        self.assertEqual(expected_result, result)


if __name__ == '__main__':
    unittest.main()
