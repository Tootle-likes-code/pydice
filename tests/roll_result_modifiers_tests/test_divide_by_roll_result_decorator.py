import unittest
from unittest.mock import Mock, PropertyMock

from pydice.roll_result_operators.roll_result_decorators import DivideByRollResultDecorator


class DivideByRollResultDecoratorTests(unittest.TestCase):
    def setUp(self) -> None:
        self.test_die_result = Mock()
        self.test_die_result.result = Mock(return_value=4)
        self.test_die_result.die_rolls = PropertyMock(return_value=[4, 5])

        self.test_roll_result = DivideByRollResultDecorator(self.test_die_result, 2)


class DieRollsTests(DivideByRollResultDecoratorTests):
    def test_rolled_values_are_returned(self):
        # Arrange
        expected_result = [4, 5]

        # Act
        result = self.test_roll_result.die_rolls()

        # Assert
        self.assertEqual(expected_result, result)


class ResultsTests(DivideByRollResultDecoratorTests):
    def test_result_is_divided_correctly(self):
        # Arrange
        expected_result = 2

        # Act
        result = self.test_roll_result.result()

        # Assert
        self.assertEqual(expected_result, result)

    def test_remainder_result_is_rounded_up_correctly(self):
        # Arrange
        expected_result = 1
        test_roll_result = DivideByRollResultDecorator(self.test_die_result, 5)

        # Act
        result = test_roll_result.result()

        # Assert
        self.assertEqual(expected_result, result)

    def test_remainder_result_is_rounded_down_correctly(self):
        # Arrange
        expected_result = 1
        test_roll_result = DivideByRollResultDecorator(self.test_die_result, 3)

        # Act
        result = test_roll_result.result()

        # Assert
        self.assertEqual(expected_result, result)

    def test_results_calls_decorated_results(self):
        # Act
        self.test_roll_result.result()

        # Assert
        self.test_die_result.result.assert_called_once()


if __name__ == '__main__':
    unittest.main()
