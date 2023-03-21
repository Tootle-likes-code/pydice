import unittest
from unittest.mock import MagicMock

from pydice.die import Die
from pydice.roll_result import DieRollResult


class DieRollResultTests(unittest.TestCase):
    def setUp(self) -> None:
        self.test_die = MagicMock(spec=Die)
        self.test_die.min = 1
        self.test_die.max = 6
        self.test_die.roll = MagicMock(return_value=[5])

        self.test_die_roll_result = DieRollResult(self.test_die, 3)


class DieTests(DieRollResultTests):
    def test_can_get_value(self):
        # Assert
        self.assertEqual(self.test_die_roll_result.die, self.test_die)

    def test_cannot_set_value(self):
        # Assert
        with self.assertRaises(AttributeError) as ex:
            # Act
            self.test_die_roll_result.die = 123


class DieRollsTests(DieRollResultTests):
    def test_returns_die_roll(self):
        # Arrange
        expected_result = [3]

        # Act
        result = self.test_die_roll_result.die_rolls

        # Assert
        self.assertEqual(expected_result, result)

    def test_if_roll_not_provided_rolls_die(self):
        # Act
        DieRollResult(self.test_die)

        # Assert
        self.test_die.roll.assert_called_once()

    def test_if_roll_not_provided_rolls_die_roll_is_updated(self):
        # Assert
        expected_result = 5

        # Act
        test_die_result = DieRollResult(self.test_die)

        # Assert
        self.assertEqual(expected_result, test_die_result._roll)

    def test_if_roll_not_provided_die_rolls_is_updated(self):
        # Assert
        expected_result = [5]

        # Act
        test_die_result = DieRollResult(self.test_die)

        # Assert
        self.assertEqual(expected_result, test_die_result.die_rolls)

    def test_if_roll_provided_die_is_not_rolled(self):
        # Act
        DieRollResult(self.test_die, 4)

        # Assert
        self.test_die.roll.assert_not_called()


class ResultTests(DieRollResultTests):
    def test_returns_die_roll(self):
        # Arrange
        expected_result = 3

        # Act
        result = self.test_die_roll_result.result

        # Assert
        self.assertEqual(expected_result, result)


if __name__ == '__main__':
    unittest.main()
