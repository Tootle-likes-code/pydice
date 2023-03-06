import unittest
from unittest.mock import patch, call

from pydice.die import Die


class DieTests(unittest.TestCase):
    def setUp(self) -> None:
        self.test_die = Die(6)


@patch("pydice.die.random.randint", return_value=3)
class RollTests(DieTests):
    def test_min_and_max_are_being_used_for_random(self, mock_random):
        # Arrange
        expected_calls = [call(1, 6)]

        # Act
        self.test_die.roll()

        # Assert
        mock_random.assert_called_once()
        mock_random.assert_has_calls(expected_calls)

    def test_min_and_max_are_being_used_for_random(self, mock_random):
        # Arrange
        expected_calls = [call(-2, 3)]
        test_die = Die(6, -2)

        # Act
        test_die.roll()

        # Assert
        mock_random.assert_called_once()
        mock_random.assert_has_calls(expected_calls)


class MinTests(DieTests):
    def test_min_returns_min_value(self):
        # Arrange
        expected_result = 1
        test_die = Die(6, 1)

        # Act
        result = test_die.min

        # Assert
        self.assertEqual(expected_result, result)

    def test_negative_min_returns_negative_min_value(self):
        # Arrange
        expected_result = -10
        test_die = Die(6, -10)

        # Act
        result = test_die.min

        # Assert
        self.assertEqual(expected_result, result)

    def test_updated_minimum_roll_reflects_in_min(self):
        # Arrange
        expected_result = -1
        test_die = Die(6)

        # Act
        test_die._minimum_roll = -1

        # Assert
        self.assertEqual(expected_result, test_die.min)


class MaxTests(DieTests):
    def test_max_returns_expected_value(self):
        # Arrange
        expected_result = 6
        test_die = self.test_die

        # Act
        result = test_die.max

        # Assert
        self.assertEqual(expected_result, result)

    def test_max_is_incremental_of_negative_min(self):
        # Arrange
        expected_result = 3
        test_die = Die(6, -2)

        # Act
        result = test_die.max

        # Assert
        self.assertEqual(expected_result, result)

    def test_max_is_incremental_of_min_greater_than_zero(self):
        # Arrange
        expected_result = 7
        test_die = Die(6, 2)

        # Act
        result = test_die.max

        # Assert
        self.assertEqual(expected_result, result)

    def test_max_is_called_after_minimum_roll_is_changed_correctly_represents_new_max(self):
        # Arrange
        expected_result = 5
        test_die = Die(6)

        # Act
        test_die._minimum_roll = 0
        result = test_die.max

        # Assert
        self.assertEqual(expected_result, result)


class StrTests(DieTests):
    def test_default_die_result_is_expected_string(self):
        # Arrange
        expected_result = "D6"

        # Act
        result = str(self.test_die)

        # Assert
        self.assertEqual(expected_result, result)

    def test_die_with_new_min_is_expected_string(self):
        # Arrange
        expected_result = "D6[-1-4]"
        test_die = Die(6, -1)

        # Act
        result = str(test_die)

        # Assert
        self.assertEqual(expected_result, result)


if __name__ == '__main__':
    unittest.main()
