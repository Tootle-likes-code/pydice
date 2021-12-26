import unittest
from unittest.mock import Mock, PropertyMock

from roll_result import AddToRollResultDecorator


class AddToRollResultDecoratorTests(unittest.TestCase):
    def setUp(self) -> None:
        self.test_die = Mock()
        self.test_die.result = Mock(return_value=3)
        self.test_die.die_rolls = PropertyMock(return_value=[4, 5])

        self.test_roll_result = AddToRollResultDecorator(self.test_die, 2)


class DieRollsTests(AddToRollResultDecoratorTests):
    def test_rolled_values_are_returned(self):
        # Arrange
        expected_result = [4, 5]

        # Act
        result = self.test_roll_result.die_rolls()

        # Assert
        self.assertEqual(expected_result, result)


class ResultTests(AddToRollResultDecoratorTests):
    def test_results_has_modifier_added_to_it(self):
        # Arrange
        expected_result = 5

        # Act
        result = self.test_roll_result.result()

        # Assert
        self.assertEqual(expected_result, result)


if __name__ == '__main__':
    unittest.main()
