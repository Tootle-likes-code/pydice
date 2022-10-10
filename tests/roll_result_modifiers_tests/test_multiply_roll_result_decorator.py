import unittest
from unittest.mock import Mock, PropertyMock

from pydice.roll_result_operators.roll_result_decorators import MultiplyRollResultDecorator


class MultiplyRollResultDecoratorTests(unittest.TestCase):
    def setUp(self) -> None:
        self.test_die_result = Mock()
        self.test_die_result.result = 5
        self.test_die_result.die_rolls = [4, 5]

        self.test_roll_result = MultiplyRollResultDecorator(self.test_die_result, 2)


class ConstructorTests(MultiplyRollResultDecoratorTests):
    def setUp(self) -> None:
        self.test_die_result = Mock()
        self.test_die_result_result = PropertyMock(return_value=5)
        type(self.test_die_result).result = self.test_die_result_result


    def test_results_calls_decorated_results(self):
        # Act
        MultiplyRollResultDecorator(self.test_die_result, 5)

        # Assert
        self.test_die_result_result.assert_called_once()


class DieRollsTests(MultiplyRollResultDecoratorTests):
    def test_rolled_values_are_returned(self):
        # Arrange
        expected_result = [4, 5]

        # Act
        result = self.test_roll_result.die_rolls

        # Assert
        self.assertEqual(expected_result, result)


class ResultTests(MultiplyRollResultDecoratorTests):
    def test_result_is_multiplied_correctly(self):
        # Arrange
        expected_result = 10

        # Act
        result = self.test_roll_result.result

        # Assert
        self.assertEqual(expected_result, result)


if __name__ == '__main__':
    unittest.main()
