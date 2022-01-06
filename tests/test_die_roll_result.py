import unittest
from unittest.mock import MagicMock

from pydice.die import Die
from pydice.roll_result import DieRollResult


class DieRollResultTests(unittest.TestCase):
    def setUp(self) -> None:
        self.test_die = MagicMock(spec=Die)
        self.test_die.min = 1
        self.test_die.max = 6

        self.test_die_roll_result = DieRollResult(self.test_die, 3)


class DieRollsTests(DieRollResultTests):
    def test_returns_die_roll(self):
        # Arrange
        expected_result = [3]

        # Act
        result = self.test_die_roll_result.die_rolls

        # Assert
        self.assertEqual(expected_result, result)


class ResultTests(DieRollResultTests):
    def test_returns_die_roll(self):
        # Arrange
        expected_result = 3

        # Act
        result = self.test_die_roll_result.result()

        # Assert
        self.assertEqual(expected_result, result)


class AddRollResultTests(DieRollResultTests):
    def test_adds_new_value_to_rolls(self):
        # Arrange
        expected_result = [3, 4]

        # Act
        self.test_die_roll_result.add_die_roll(4)
        result = self.test_die_roll_result.die_rolls

        # Assert
        self.assertEqual(expected_result, result)

    def test_adding_value_below_min_raises_Value_Error(self):
        # Arrange
        expected_args = ('Roll must be less than min and greater than max. Die Min: 1, Die Max: 6, '
                         'value to add: -50',)

        # Act
        with self.assertRaises(ValueError) as ex:
            self.test_die_roll_result.add_die_roll(-50)

        # Assert
        self.assertEqual(expected_args, ex.exception.args)

    def test_adding_value_below_max_raises_Value_Error(self):
        # Arrange
        expected_args = ('Roll must be less than min and greater than max. Die Min: 1, Die Max: 6, '
                         'value to add: 50',)

        # Act
        with self.assertRaises(ValueError) as ex:
            self.test_die_roll_result.add_die_roll(50)

        # Assert
        self.assertEqual(expected_args, ex.exception.args)

    def test_adding_min_adds_value(self):
        # Arrange
        expected_result = [3, 1]

        # Act
        self.test_die_roll_result.add_die_roll(1)
        result = self.test_die_roll_result.die_rolls

        # Assert
        self.assertEqual(expected_result, result)

    def test_adding_max_adds_value(self):
        # Arrange
        expected_result = [3, 6]

        # Act
        self.test_die_roll_result.add_die_roll(6)
        result = self.test_die_roll_result.die_rolls

        # Assert
        self.assertEqual(expected_result, result)


if __name__ == '__main__':
    unittest.main()
