import unittest
from unittest.mock import Mock, PropertyMock

from pydice.roll_result_operators.roll_result_decorators import SubtractFromRollResultDecorator


class SubtractFromRollResultDecoratorTests(unittest.TestCase):
    def setUp(self) -> None:
        self.test_die_result = Mock()
        self.test_die_result.result = 3
        self.test_die_result.die_rolls = [4, 5]

        self.test_roll_result = SubtractFromRollResultDecorator(self.test_die_result, 2)


class ConstructorTests(SubtractFromRollResultDecoratorTests):
    def setUp(self) -> None:
        self.test_die_result = Mock()
        self.test_die_result_result = PropertyMock(return_value=3)
        type(self.test_die_result).result = self.test_die_result_result

    def test_results_calls_decorated_results(self):
        # Act
        SubtractFromRollResultDecorator(self.test_die_result, 3)

        # Assert
        self.test_die_result_result.assert_called_once()


class DieRollsTests(SubtractFromRollResultDecoratorTests):
    def test_rolled_values_are_returned(self):
        # Arrange
        expected_result = [4, 5]

        # Act
        result = self.test_roll_result.die_rolls

        # Assert
        self.assertEqual(expected_result, result)


class ResultTests(SubtractFromRollResultDecoratorTests):
    def test_results_has_modifier_added_to_it(self):
        # Arrange
        expected_result = 1

        # Act
        result = self.test_roll_result.result

        # Assert
        self.assertEqual(expected_result, result)


if __name__ == '__main__':
    unittest.main()
