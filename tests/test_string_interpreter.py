import unittest
from unittest.mock import patch

from pydice.die import Dice, Die, FateDie
from pydice.roll_result import AddToRollResultDecorator, RollResultDecorator, DiceRollResult, \
    SubtractFromRollResultDecorator, MultiplyRollResultDecorator, DivideByRollResultDecorator
from pydice.dice_string_interpreter import interpret

dice_results = [9, 10, 6, 7, 6, 1, 2, 4, 8, 3]
default_fate_result = [-1, 1, 0, 0]


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


if __name__ == '__main__':
    unittest.main()
