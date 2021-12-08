import unittest
from unittest.mock import MagicMock

from die import Dice


class DiceTests(unittest.TestCase):
    def setUp(self) -> None:
        pass


class RollTests(DiceTests):
    def test_roll_result_is_as_expected(self):
        # Arrange
        expected_result = [4, 3]

        mock_die = MagicMock()
        mock_die.roll.side_effect = [4, 3]
        dice = Dice(mock_die, 2)

        # Act
        result = dice.roll()

        # Assert
        self.assertEqual(expected_result, result)


if __name__ == '__main__':
    unittest.main()
