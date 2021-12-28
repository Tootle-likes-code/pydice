import unittest
from unittest.mock import MagicMock, Mock

from die import Die
from roll_result import DieRollResult


class DieRollResultTests(unittest.TestCase):
    def setUp(self) -> None:
        self.test_die = MagicMock(spec=Die)

        self.test_die_roll_result = DieRollResult(self.test_die, 3)


class RollResultTests(DieRollResultTests):
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


if __name__ == '__main__':
    unittest.main()
