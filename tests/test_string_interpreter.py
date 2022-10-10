import unittest
from unittest import skip
from unittest.mock import patch

from pydice.dice_string.dice_string_interpreter import interpret
from pydice.die import Dice, Die, FateDie
from pydice.roll_result import AddToRollResultDecorator, DiceRollResult, \
    SubtractFromRollResultDecorator, MultiplyRollResultDecorator, DivideByRollResultDecorator, \
    CountValuesEqualToDecorator, ExplodeDiceForTargetDecorator, \
    CountValuesGreaterThanDecorator, CountValuesLessThanDecorator, CountValuesNotEqualToDecorator

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

    def test_interpret_with_simple_roll_returns_correct_value(self, _):
        # Arrange
        expected_result = DiceRollResult(self.d20, self._default_roll_result)

        # Act
        result = interpret("1d20")

        # Assert
        self.assertEqual(expected_result, result)

    def test_interpret_with_numberless_d20_returns_correct_dice(self, _):
        # Arrange
        expected_result = DiceRollResult(self.d20, self._default_roll_result)

        # Act
        result = interpret("d20")

        # Assert
        self.assertEqual(expected_result, result)

    def test_interpret_with_ten_d10_returns_correct_dice(self, _):
        # Arrange
        expected_result = DiceRollResult(Dice(number_of_dice=10, die=Die(10)), dice_results)

        # Act
        result = interpret("10d10")

        # Assert
        self.assertEqual(expected_result, result)

    def test_interpret_d_case_does_not_matter(self, _):
        # Arrange
        expected_result = DiceRollResult(self.d20, self._default_roll_result)

        # Act
        result = interpret("1D20")

        # Assert
        self.assertEqual(expected_result, result)

    def test_interpret_add_adds_decorator(self, _):
        # Arrange
        expected_result = AddToRollResultDecorator(DiceRollResult(self.d20, self._default_roll_result), 5)

        # Act
        result = interpret("1d20+5")

        # Assert
        self.assertEqual(expected_result, result)

    def test_interpret_adding_twice_adds_decorator_twice(self, _):
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

        # Act
        result = interpret("1d20+5+6")

        # Assert
        self.assertEqual(expected_result, result)

    def test_interpret_subtract_adds_decorator(self, _):
        # Arrange
        expected_result = SubtractFromRollResultDecorator(DiceRollResult(self.d20, self._default_roll_result), 5)

        # Act
        result = interpret("1d20-5")

        # Assert
        self.assertEqual(expected_result, result)

    def test_interpret_multiply_adds_decorator(self, _):
        # Arrange
        expected_result = MultiplyRollResultDecorator(DiceRollResult(self.d20, self._default_roll_result), 5)

        # Act
        result = interpret("1d20*5")

        # Assert
        self.assertEqual(expected_result, result)

    def test_interpret_divide_adds_decorator(self, _):
        # Arrange
        expected_result = DivideByRollResultDecorator(DiceRollResult(self.d20, self._default_roll_result), 5)

        # Act
        result = interpret("1d20/5")

        # Assert
        self.assertEqual(expected_result, result)

    def test_interpret_equal_to_adds_decorator(self, _):
        # Arrange
        expected_result = CountValuesEqualToDecorator(DiceRollResult(self.d20, self._default_roll_result), 9)

        # Act
        result = interpret("1d20=9")

        # Assert
        self.assertEqual(expected_result, result)

    def test_interpret_greater_than_adds_decorator(self, _):
        # Arrange
        expected_result = CountValuesGreaterThanDecorator(DiceRollResult(self.d20, self._default_roll_result), 9)

        # Act
        result = interpret("1d20>9")

        # Assert
        self.assertEqual(expected_result, result)

    def test_interpret_greater_than_equal_to_adds_greater_than_and_equal_to_decorator(self, _):
        # Arrange
        expected_result = CountValuesGreaterThanDecorator(
            CountValuesEqualToDecorator(
                DiceRollResult(self.d20, self._default_roll_result), 15
            ), 15
        )

        # Act
        result = interpret("1d20>=15")

        # Assert
        self.assertEqual(expected_result, result)

    def test_interpret_less_than_adds_decorator(self, _):
        # Arrange
        expected_result = CountValuesLessThanDecorator(DiceRollResult(self.d20, self._default_roll_result), 9)

        # Act
        result = interpret("1d20<9")

        # Assert
        self.assertEqual(expected_result, result)

    def test_interpret_less_than_equal_to_adds_decorator(self, _):
        # Arrange
        expected_result = CountValuesLessThanDecorator(
            CountValuesEqualToDecorator(
                DiceRollResult(self.d20, self._default_roll_result), 9
            ), 9
        )

        # Act
        result = interpret("1d20<=9")

        # Assert
        self.assertEqual(expected_result, result)

    def test_interpret_not_equal_to_adds_decorator(self, _):
        # Arrange
        expected_result = CountValuesNotEqualToDecorator(DiceRollResult(self.d20, self._default_roll_result), 9)

        # Act
        result = interpret("1d20!=9")

        # Assert
        self.assertEqual(expected_result, result)

    def test_interpret_not_equal_to_alt_adds_decorator(self, _):
        # Arrange
        expected_result = CountValuesNotEqualToDecorator(DiceRollResult(self.d20, self._default_roll_result), 9)

        # Act
        result = interpret("1d20=/=9")

        # Assert
        self.assertEqual(expected_result, result)

    def test_interpret_explodes_adds_decorator(self, mock_die_rolls):
        # Arrange
        expected_result = ExplodeDiceForTargetDecorator(DiceRollResult(Dice(Die(10), 14),
                                                                       default_story_teller_dice_results[:-1]), 10)
        mock_die_rolls.side_effect = default_story_teller_dice_results

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


@patch("pydice.die.random.randint", side_effect=default_fate_result)
class InterpretWithFateTests(StringInterpreterTests):
    def setUp(self) -> None:
        self.fate_dice = Dice(FateDie(), 4)

    def test_interpret_fate_die_rolls_four_dice(self, _):
        # Arrange
        expected_result = DiceRollResult(self.fate_dice, default_fate_result)

        # Act
        result = interpret("df")

        # Assert
        self.assertEqual(expected_result, result)

    def test_interpret_fate_die_with_add_is_added(self, _):
        # Arrange
        expected_result = AddToRollResultDecorator(DiceRollResult(self.fate_dice, default_fate_result), 2)

        # Act
        result = interpret("df+2")

        # Assert
        self.assertEqual(expected_result, result)

    def test_interpret_fate_die_case_insensitive(self, _):
        # Arrange
        expected_result = DiceRollResult(self.fate_dice, default_fate_result)

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
        expected_result = CountValuesGreaterThanDecorator(
            CountValuesEqualToDecorator(
                CountValuesEqualToDecorator(
                    DiceRollResult(self._test_dice, default_story_teller_dice_results), 10),
                7),
            7)

        # Act
        result = interpret("15st")

        # Assert
        self.assertEqual(expected_result, result)

    def test_storyteller_dice_adding_successes_correctly_interpreted(self, _):
        # Arrange
        expected_result = AddToRollResultDecorator(
            CountValuesGreaterThanDecorator(
                CountValuesEqualToDecorator(
                    CountValuesEqualToDecorator(
                        DiceRollResult(self._test_dice, default_story_teller_dice_results), 10),
                    7),
                7),
            7)

        # Act
        result = interpret("15st+7")

        # Assert
        self.assertEqual(expected_result, result)

    def test_storyteller_case_insensitive(self, _):
        # Arrange
        expected_result = CountValuesGreaterThanDecorator(
            CountValuesEqualToDecorator(
                CountValuesEqualToDecorator(
                    DiceRollResult(self._test_dice, default_story_teller_dice_results), 10),
                7),
            7)

        # Act
        result = interpret("15ST")

        # Assert
        self.assertEqual(expected_result, result)


if __name__ == '__main__':
    unittest.main()
