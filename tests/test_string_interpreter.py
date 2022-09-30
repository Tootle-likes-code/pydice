import unittest

from pydice.die import Dice, Die
from pydice.string_interpreter import interpret


class StringInterpreterTests(unittest.TestCase):
    def test_interpret_with_simple_roll_returns_correct_value(self):
        # Arrange
        expected_result = Dice(number_of_dice=1, die=Die(20))

        # Act
        result = interpret("1d20")

        # Assert
        self.assertEqual(expected_result, result)

    def test_interpret_with_numberless_d20_returns_correct_dice(self):
        # Arrange
        expected_result = Dice(number_of_dice=1, die=Die(20))

        # Act
        result = interpret("d20")

        # Assert
        self.assertEqual(expected_result, result)

    def test_interpret_with_ten_d10_returns_correct_dice(self):
        # Arrange
        expected_result = Dice(number_of_dice=10, die=Die(10))

        # Act
        result = interpret("10d10")

        # Assert
        self.assertEqual(expected_result, result)

    def test_interpret_d_case_does_not_matter(self):
        # Arrange
        expected_result = Dice(number_of_dice=1, die=Die(20))

        # Act
        result = interpret("1D20")

        # Assert
        self.assertEqual(expected_result, result)


if __name__ == '__main__':
    unittest.main()
